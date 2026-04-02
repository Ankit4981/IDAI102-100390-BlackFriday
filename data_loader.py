"""
Data module — loads Black Friday dataset or generates synthetic sample data.
"""

import os
import logging
import pandas as pd
import numpy as np
import streamlit as st

# ── reproducible seed ──────────────────────────────────────────────
SEED = 42

logger = logging.getLogger(__name__)

# ── Candidate paths for BlackFriday.csv ───────────────────────────
# Look next to this script first, then in cwd
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_SEARCH_PATHS = [
    os.path.join(_SCRIPT_DIR, "BlackFriday.csv"),
    os.path.join(_SCRIPT_DIR, "blackfriday.csv"),
    os.path.join(_SCRIPT_DIR, "black_friday.csv"),
    "BlackFriday.csv",
    "blackfriday.csv",
    "black_friday.csv",
]


@st.cache_data(show_spinner=False)
def generate_sample_data(n: int = 10_000) -> pd.DataFrame:
    """
    Generate a realistic Black Friday synthetic dataset when the real
    CSV is not available.  Schema mirrors the Kaggle Black Friday dataset.
    """
    rng = np.random.default_rng(SEED)

    user_ids    = rng.integers(1_000_000, 1_010_000, n)
    product_ids = ["P" + str(rng.integers(10_000, 99_999)) for _ in range(n)]

    genders   = rng.choice(["M", "F"], n, p=[0.75, 0.25])
    age_bins  = ["0-17","18-25","26-35","36-45","46-50","51-55","55+"]
    age_probs = [0.03, 0.20, 0.35, 0.22, 0.10, 0.06, 0.04]
    ages      = rng.choice(age_bins, n, p=age_probs)

    occupations = rng.integers(0, 21, n)
    city_cats   = rng.choice(["A","B","C"], n, p=[0.25, 0.40, 0.35])
    stay_yrs    = rng.choice([0,1,2,3,4], n, p=[0.15,0.20,0.25,0.25,0.15])
    marital     = rng.integers(0, 2, n)

    cat1 = rng.integers(1, 21, n)

    # Product_Category_2: ~70 % populated, rest NaN
    cat2 = rng.integers(2, 19, n).astype(float)
    cat2[rng.random(n) < 0.30] = np.nan

    # Product_Category_3: ~40 % populated, rest NaN
    cat3 = rng.integers(3, 19, n).astype(float)
    cat3[rng.random(n) < 0.60] = np.nan

    base_purchase = rng.lognormal(mean=8.5, sigma=0.8, size=n).astype(int)
    base_purchase = np.clip(base_purchase, 185, 23_961)

    return pd.DataFrame({
        "User_ID":                    user_ids,
        "Product_ID":                 product_ids,
        "Gender":                     genders,
        "Age":                        ages,
        "Occupation":                 occupations,
        "City_Category":              city_cats,
        "Stay_In_Current_City_Years": stay_yrs,
        "Marital_Status":             marital,
        "Product_Category_1":         cat1,
        "Product_Category_2":         cat2,
        "Product_Category_3":         cat3,
        "Purchase":                   base_purchase,
    })


@st.cache_data(show_spinner=False)
def load_data(uploaded_file=None) -> tuple[pd.DataFrame, str]:
    """
    Load dataset from:
      1. User-uploaded file (CSV / Excel)
      2. BlackFriday.csv searched next to app.py AND in cwd
      3. Synthetic fallback

    Returns (dataframe, source_label).
    """
    # 1 — uploaded file
    if uploaded_file is not None:
        try:
            if uploaded_file.name.lower().endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            logger.info("Loaded uploaded file: %s", uploaded_file.name)
            return _clean(df), f"Uploaded: {uploaded_file.name}"
        except Exception as exc:
            logger.warning("Could not read upload: %s", exc)
            st.warning(f"Could not read upload: {exc}. Trying local file...")

    # 2 — search for local CSV
    for fpath in CSV_SEARCH_PATHS:
        if os.path.exists(fpath):
            try:
                df = pd.read_csv(fpath)
                logger.info("Loaded local file: %s", fpath)
                return _clean(df), f"BlackFriday Dataset ({os.path.basename(fpath)})"
            except Exception as exc:
                logger.warning("Could not read %s: %s", fpath, exc)

    # 3 — synthetic fallback (only if CSV truly not found)
    logger.warning("BlackFriday.csv not found — using synthetic data")
    st.info(
        "BlackFriday.csv not found. Place it in the same folder as app.py "
        "to use the real dataset. Running on synthetic sample data (10K rows).",
    )
    df = generate_sample_data(10_000)
    return df, "Synthetic Sample Data (10 K rows)"


def _clean(df: pd.DataFrame) -> pd.DataFrame:
    """
    Basic cleaning applied to every loaded dataframe:
      - Drop fully duplicate rows
      - Ensure Purchase is numeric, drop null Purchase rows
      - Fill sparse product-category columns with 0
    """
    df = df.drop_duplicates()

    df["Purchase"] = pd.to_numeric(df["Purchase"], errors="coerce")
    df = df.dropna(subset=["Purchase"])

    for col in ["Product_Category_2", "Product_Category_3"]:
        if col in df.columns:
            df[col] = df[col].fillna(0).astype(int)

    return df.reset_index(drop=True)


def get_summary(df: pd.DataFrame) -> dict:
    """Return high-level statistics for KPI cards."""
    return {
        "rows":            len(df),
        "columns":         len(df.columns),
        "total_revenue":   int(df["Purchase"].sum()),
        "avg_purchase":    round(float(df["Purchase"].mean()), 2),
        "unique_users":    df["User_ID"].nunique() if "User_ID" in df.columns else 0,
        "unique_products": df["Product_ID"].nunique() if "Product_ID" in df.columns else 0,
        "missing_pct":     round(df.isnull().mean().mean() * 100, 2),
        "gender_m_pct":    round((df["Gender"] == "M").mean() * 100, 1)
                           if "Gender" in df.columns else 0,
    }
