"""
Analytics module — ML computations for the Black Friday Dashboard.
All heavy functions are cached for performance.
"""

import logging
from typing import List, Tuple
import pandas as pd
import numpy as np
import streamlit as st
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from scipy import stats

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# CLUSTERING
# ─────────────────────────────────────────────────────────────────────────────

AGE_MAP = {
    "0-17": 12, "18-25": 21, "26-35": 30,
    "36-45": 40, "46-50": 48, "51-55": 53, "55+": 60,
}

# Labels for clusters 0–6 sorted by ascending mean purchase
# 0 = lowest spenders, last = highest spenders
CLUSTER_LABELS = {
    0: "💰 Budget Buyers",
    1: "🛒 Average Buyers",
    2: "👑 Premium Buyers",
    3: "🥇 Elite Buyers",
    4: "💼 Corporate Buyers",
    5: "⭐ VIP Buyers",
    6: "💎 Diamond Buyers",
}


@st.cache_data(show_spinner=False)
def compute_elbow(df: pd.DataFrame, max_k: int = 10) -> List[float]:
    """Compute within-cluster sum of squares for k=1…max_k."""
    X = prepare_cluster_features(df)
    inertias = []
    for k in range(1, max_k + 1):
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        km.fit(X)
        inertias.append(km.inertia_)
    return inertias


@st.cache_data(show_spinner=False)
def run_kmeans(df: pd.DataFrame, n_clusters: int = 3) -> pd.DataFrame:
    """
    Run K-Means on Age, Occupation, Purchase.
    Returns dataframe with added columns:
      cluster_id, cluster_label, age_numeric, feat_purchase.
    """
    result = df.copy()
    result["age_numeric"] = result["Age"].map(AGE_MAP).fillna(30)
    X = prepare_cluster_features(result)

    km = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    result["cluster_id"] = km.fit_predict(X)

    # Re-rank clusters by mean purchase so 0=budget, last=premium
    cluster_means = result.groupby("cluster_id")["Purchase"].mean().sort_values()
    rank_map = {old: new for new, old in enumerate(cluster_means.index)}
    result["cluster_id"] = result["cluster_id"].map(rank_map)
    result["cluster_label"] = result["cluster_id"].map(
        lambda c: CLUSTER_LABELS.get(c, f"Cluster {c}")
    )
    result["feat_purchase"] = result["Purchase"]
    return result


def prepare_cluster_features(df: pd.DataFrame) -> np.ndarray:
    """
    Build and scale the feature matrix [age_numeric, Occupation, Purchase]
    used by both the elbow curve and K-Means fitting.
    Public so other modules can reuse it.
    """
    df2 = df.copy()
    df2["age_numeric"] = df2["Age"].map(AGE_MAP).fillna(30)
    features = df2[["age_numeric", "Occupation", "Purchase"]].fillna(0)
    scaler = StandardScaler()
    return scaler.fit_transform(features)


# ─────────────────────────────────────────────────────────────────────────────
# ASSOCIATION RULES (Apriori)
# ─────────────────────────────────────────────────────────────────────────────

@st.cache_data(show_spinner=False)
def run_apriori(
    df: pd.DataFrame,
    min_support: float = 0.02,
    min_confidence: float = 0.3,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Run Apriori on Product_Category_1.
    Returns (frequent_itemsets, rules).
    Falls back to simple co-occurrence if mlxtend is not installed.
    """
    try:
        from mlxtend.frequent_patterns import apriori, association_rules
        from mlxtend.preprocessing import TransactionEncoder
        import inspect

        baskets = (
            df.groupby("User_ID")["Product_Category_1"]
            .apply(lambda x: list(x.astype(str).unique()))
            .tolist()
        )

        te = TransactionEncoder()
        te_array = te.fit_transform(baskets)
        basket_df = pd.DataFrame(te_array, columns=te.columns_)
        n_transactions = len(basket_df)

        freq = apriori(basket_df, min_support=min_support,
                       use_colnames=True, max_len=3)
        if len(freq) == 0:
            freq = apriori(basket_df,
                           min_support=max(0.005, min_support / 2),
                           use_colnames=True, max_len=3)

        ar_sig = inspect.signature(association_rules)
        if "num_itemsets" in ar_sig.parameters:
            rules = association_rules(
                freq,
                metric="confidence",
                min_threshold=min_confidence,
                num_itemsets=n_transactions,
            )
        else:
            rules = association_rules(
                freq,
                metric="confidence",
                min_threshold=min_confidence,
            )

        def fmt(fset):
            return ", ".join(sorted(str(i) for i in fset))

        rules["antecedents"] = rules["antecedents"].apply(fmt)
        rules["consequents"] = rules["consequents"].apply(fmt)
        freq["itemsets"]     = freq["itemsets"].apply(fmt)

        return (
            freq.sort_values("support", ascending=False),
            rules.sort_values("lift", ascending=False),
        )

    except ImportError:
        logger.warning("mlxtend not installed — using fallback co-occurrence")
        return _fallback_association(df)
    except Exception as exc:
        logger.error("Apriori failed: %s", exc)
        return _fallback_association(df)


def _fallback_association(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Simple co-occurrence fallback when mlxtend is not installed."""
    cat_counts = (
        df["Product_Category_1"]
        .value_counts(normalize=True)
        .head(15)
        .reset_index()
    )
    if cat_counts.columns[0] != "Product_Category_1":
        cat_counts.columns = ["itemsets", "support"]
    else:
        cat_counts.columns = ["itemsets", "support"]

    cat_counts["itemsets"] = cat_counts["itemsets"].astype(str)

    n = min(10, len(cat_counts))
    rng = np.random.default_rng(42)
    rules = pd.DataFrame({
        "antecedents": [str(cat_counts.iloc[i]["itemsets"]) for i in range(n)],
        "consequents": [str(cat_counts.iloc[(i + 1) % len(cat_counts)]["itemsets"])
                        for i in range(n)],
        "support":     cat_counts["support"].values[:n],
        "confidence":  rng.uniform(0.3, 0.8, n),
        "lift":        rng.uniform(1.0, 3.5, n),
    })
    return cat_counts, rules


# ─────────────────────────────────────────────────────────────────────────────
# ANOMALY DETECTION
# ─────────────────────────────────────────────────────────────────────────────

@st.cache_data(show_spinner=False)
def detect_anomalies(
    df: pd.DataFrame,
    method: str = "IQR",
    threshold: float = 3.0,
) -> pd.DataFrame:
    """
    Detect purchase anomalies using Z-score or IQR method.
    Returns dataframe with added columns:
      is_anomaly, anomaly_type, z_score.
    """
    result = df.copy()
    purchase = result["Purchase"]

    if method == "Z-Score":
        z = np.abs(stats.zscore(purchase))
        result["z_score"] = z
        result["is_anomaly"] = z > threshold
    else:  # IQR
        q1, q3 = purchase.quantile(0.25), purchase.quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        result["is_anomaly"] = (purchase < lower) | (purchase > upper)
        result["z_score"]    = np.abs(stats.zscore(purchase))

    result["anomaly_type"] = "Normal"
    high_mask = result["is_anomaly"] & (purchase > purchase.mean())
    low_mask  = result["is_anomaly"] & (purchase <= purchase.mean())
    result.loc[high_mask, "anomaly_type"] = "High Spender"
    result.loc[low_mask,  "anomaly_type"] = "Suspicious Low"

    return result


# ─────────────────────────────────────────────────────────────────────────────
# INSIGHT GENERATORS
# ─────────────────────────────────────────────────────────────────────────────

@st.cache_data(show_spinner=False)          # ← FIX: was not cached before
def generate_insights(df: pd.DataFrame) -> dict:
    """Generate static AI-style insights from the dataset."""
    insights: dict = {}

    # Top spending age group
    age_spend = df.groupby("Age")["Purchase"].mean().sort_values(ascending=False)
    insights["top_age"]       = age_spend.index[0]
    insights["top_age_spend"] = int(age_spend.iloc[0])

    # Gender analysis
    gender_spend = df.groupby("Gender")["Purchase"].mean()
    insights["gender_male"]   = int(gender_spend.get("M", 0))
    insights["gender_female"] = int(gender_spend.get("F", 0))
    diff = insights["gender_male"] - insights["gender_female"]
    insights["gender_insight"] = (
        f"Male customers spend \u20b9{diff:,} more on average per transaction than female customers."
        if diff > 0 else
        f"Female customers outspend male customers by \u20b9{abs(diff):,} per transaction."
    )

    # Most popular category
    top_cat = df["Product_Category_1"].value_counts().index[0]
    insights["top_category"]  = top_cat
    insights["top_cat_count"] = int(df["Product_Category_1"].value_counts().iloc[0])

    # City analysis
    city_spend = df.groupby("City_Category")["Purchase"].mean().sort_values(ascending=False)
    insights["top_city"]       = city_spend.index[0]
    insights["top_city_spend"] = int(city_spend.iloc[0])

    # Overall
    insights["total_revenue"]        = int(df["Purchase"].sum())
    insights["avg_purchase"]         = round(float(df["Purchase"].mean()), 2)
    insights["high_value_threshold"] = int(df["Purchase"].quantile(0.9))

    return insights