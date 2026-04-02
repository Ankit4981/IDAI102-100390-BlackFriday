"""
Charts module — all Plotly visualizations for the dashboard.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# ── Consistent chart theme ────────────────────────────────────────────────────
TEMPLATE  = "plotly_dark"
BG        = "rgba(0,0,0,0)"
PAPER_BG  = "rgba(0,0,0,0)"
FONT      = dict(family="DM Sans", color="#EDF2F7", size=12)
COLORS    = ["#7C6EFA", "#0EE3B4", "#F5C542", "#FF5370", "#A89FFF",
             "#38BDF8", "#FB923C", "#34D399", "#F472B6", "#60A5FA"]
GRAD      = ["#7C6EFA", "#0EE3B4", "#F5C542", "#FF5370", "#A89FFF"]

# Shared axis style
_AXIS = dict(
    gridcolor="rgba(124,110,250,0.08)",
    linecolor="rgba(124,110,250,0.15)",
    tickfont=dict(color="#566380", size=11),
    title_font=dict(color="#A0ABBE", size=12),
    zerolinecolor="rgba(124,110,250,0.12)",
)


def _base_layout(**kwargs) -> dict:
    return dict(
        template=TEMPLATE,
        plot_bgcolor=BG,
        paper_bgcolor=PAPER_BG,
        font=FONT,
        margin=dict(l=44, r=22, t=48, b=44),
        title_font=dict(family="Bricolage Grotesque", size=15, color="#EDF2F7"),
        legend=dict(
            bgcolor="rgba(11,24,40,0.75)",
            bordercolor="rgba(124,110,250,0.22)",
            borderwidth=1,
            font=dict(size=11, color="#A0ABBE"),
        ),
        xaxis=_AXIS,
        yaxis=_AXIS,
        **kwargs,
    )


def _value_counts_df(series: pd.Series, normalize: bool = False) -> pd.DataFrame:
    """
    Return a two-column DataFrame ['value', 'count'] from a Series
    in a way that works across both pandas < 2.0 and pandas >= 2.0.
    """
    vc = series.value_counts(normalize=normalize).reset_index()
    # pandas >= 2.0  → columns: [series.name, 'count' | 'proportion']
    # pandas <  2.0  → columns: ['index', series.name]
    if vc.columns[0] == "index":
        vc.columns = ["value", "count"]
    else:
        vc.columns = ["value", "count"]
    return vc


# ─────────────────────────────────────────────────────────────────────────────
# EDA charts
# ─────────────────────────────────────────────────────────────────────────────

def purchase_histogram(df: pd.DataFrame) -> go.Figure:
    fig = px.histogram(
        df, x="Purchase", nbins=60,
        color_discrete_sequence=["#7C6EFA"],
        title="Purchase Amount Distribution",
        labels={"Purchase": "Purchase Amount (₹)", "count": "Frequency"},
    )
    fig.update_traces(
        marker_line_color="rgba(124,110,250,0.5)",
        marker_line_width=0.5,
        opacity=0.85,
    )
    fig.update_layout(**_base_layout())
    fig.add_vline(
        x=df["Purchase"].mean(),
        line_dash="dash",
        line_color="#F5C542",
        annotation_text=f"Mean ₹{df['Purchase'].mean():,.0f}",
        annotation_font_color="#F5C542",
        annotation_font_size=11,
    )
    return fig


def purchase_boxplot(df: pd.DataFrame) -> go.Figure:
    age_order = ["0-17","18-25","26-35","36-45","46-50","51-55","55+"]
    present   = [a for a in age_order if a in df["Age"].unique()]
    fig = px.box(
        df, x="Age", y="Purchase",
        category_orders={"Age": present},
        color="Age",
        color_discrete_sequence=GRAD * 3,
        title="Purchase Distribution by Age Group",
        labels={"Purchase": "Purchase Amount (₹)"},
    )
    fig.update_layout(**_base_layout(), showlegend=False)
    return fig


def category_bar(df: pd.DataFrame) -> go.Figure:
    cat_counts = _value_counts_df(df["Product_Category_1"]).head(15)
    cat_counts.columns = ["Category", "Count"]

    fig = px.bar(
        cat_counts, x="Category", y="Count",
        color="Count",
        color_continuous_scale=["#7C6EFA", "#0EE3B4"],
        title="Product Category Popularity",
        labels={"Category": "Product Category", "Count": "Number of Purchases"},
    )
    fig.update_layout(**_base_layout(), coloraxis_showscale=False)
    return fig


def gender_pie(df: pd.DataFrame) -> go.Figure:
    counts = _value_counts_df(df["Gender"])
    counts.columns = ["Gender", "Count"]
    counts["Gender"] = counts["Gender"].map({"M": "Male", "F": "Female"})
    fig = px.pie(
        counts, names="Gender", values="Count",
        color_discrete_sequence=["#7C6EFA", "#0EE3B4"],
        title="Gender Distribution",
        hole=0.58,
    )
    fig.update_traces(
        textinfo="percent+label",
        pull=[0.05, 0],
        marker=dict(line=dict(color="rgba(4,9,20,0.8)", width=2)),
    )
    fig.update_layout(**_base_layout())
    return fig


def city_spend_bar(df: pd.DataFrame) -> go.Figure:
    city_data = (
        df.groupby("City_Category")["Purchase"]
        .agg(["mean", "sum", "count"])
        .reset_index()
        .rename(columns={"mean": "Avg Purchase", "sum": "Total Revenue", "count": "Transactions"})
    )
    fig = px.bar(
        city_data, x="City_Category", y="Avg Purchase",
        color="City_Category",
        color_discrete_sequence=["#7C6EFA", "#0EE3B4", "#F5C542"],
        title="Average Purchase by City Category",
        text="Avg Purchase",
    )
    fig.update_traces(
        texttemplate="₹%{text:,.0f}", textposition="outside",
        marker_line_width=0,
    )
    fig.update_layout(**_base_layout(), showlegend=False)
    return fig


def correlation_heatmap(df: pd.DataFrame) -> go.Figure:
    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    corr = df[num_cols].corr()
    fig = px.imshow(
        corr,
        color_continuous_scale=["#040A14", "#7C6EFA", "#0EE3B4"],
        title="Feature Correlation Matrix",
        text_auto=".2f",
        aspect="auto",
    )
    fig.update_layout(**_base_layout())
    return fig


def age_revenue_bar(df: pd.DataFrame) -> go.Figure:
    age_order = ["0-17","18-25","26-35","36-45","46-50","51-55","55+"]
    present   = [a for a in age_order if a in df["Age"].unique()]
    age_data  = df.groupby("Age")["Purchase"].sum().reindex(present).reset_index()
    age_data.columns = ["Age", "Total Revenue"]
    fig = px.bar(
        age_data, x="Age", y="Total Revenue",
        color="Total Revenue",
        color_continuous_scale=["#7C6EFA", "#0EE3B4"],
        title="Total Revenue by Age Group",
    )
    fig.update_traces(marker_line_width=0)
    fig.update_layout(**_base_layout(), coloraxis_showscale=False)
    return fig


def occupation_scatter(df: pd.DataFrame) -> go.Figure:
    occ_data = df.groupby("Occupation")["Purchase"].agg(["mean", "count"]).reset_index()
    occ_data.columns = ["Occupation", "Avg Purchase", "Count"]
    fig = px.scatter(
        occ_data, x="Occupation", y="Avg Purchase",
        size="Count", color="Avg Purchase",
        color_continuous_scale=["#7C6EFA", "#0EE3B4", "#F5C542"],
        title="Average Purchase by Occupation",
        labels={"Avg Purchase": "Avg Purchase (₹)"},
        hover_data=["Count"],
    )
    fig.update_layout(**_base_layout(), coloraxis_showscale=False)
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Clustering charts
# ─────────────────────────────────────────────────────────────────────────────

def elbow_chart(inertias: list[float]) -> go.Figure:
    k_vals = list(range(1, len(inertias) + 1))
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=k_vals, y=inertias,
        mode="lines+markers",
        line=dict(color="#7C6EFA", width=2.5),
        marker=dict(color="#0EE3B4", size=9, symbol="circle",
                    line=dict(color="#040A14", width=2)),
        name="Inertia",
        fill="tozeroy",
        fillcolor="rgba(124,110,250,0.05)",
    ))
    fig.update_layout(
        title="Elbow Method — Optimal k",
        xaxis_title="Number of Clusters (k)",
        yaxis_title="Within-Cluster Sum of Squares",
        **_base_layout(),
    )
    return fig


def cluster_scatter(df_clustered: pd.DataFrame) -> go.Figure:
    hover_cols = (
        ["Gender", "City_Category"]
        if "Gender" in df_clustered.columns else None
    )
    fig = px.scatter(
        df_clustered,
        x="age_numeric", y="feat_purchase",
        color="cluster_label",
        color_discrete_sequence=GRAD,
        title="Customer Segments — Age vs Purchase",
        labels={"age_numeric": "Age (numeric)", "feat_purchase": "Purchase Amount (₹)"},
        opacity=0.65,
        hover_data=hover_cols,
    )
    fig.update_traces(marker=dict(size=5, line=dict(width=0)))
    fig.update_layout(**_base_layout())
    return fig


def cluster_dist(df_clustered: pd.DataFrame) -> go.Figure:
    dist = _value_counts_df(df_clustered["cluster_label"])
    dist.columns = ["Cluster", "Count"]
    fig = px.bar(
        dist, x="Cluster", y="Count",
        color="Cluster",
        color_discrete_sequence=GRAD,
        title="Customer Count per Cluster",
        text="Count",
    )
    fig.update_traces(textposition="outside", marker_line_width=0)
    fig.update_layout(**_base_layout(), showlegend=False)
    return fig


def cluster_box(df_clustered: pd.DataFrame) -> go.Figure:
    fig = px.box(
        df_clustered, x="cluster_label", y="Purchase",
        color="cluster_label",
        color_discrete_sequence=GRAD,
        title="Purchase Distribution per Cluster",
        labels={"cluster_label": "Cluster", "Purchase": "Purchase Amount (₹)"},
    )
    fig.update_layout(**_base_layout(), showlegend=False)
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Association rule charts
# ─────────────────────────────────────────────────────────────────────────────

def rules_bar(rules: pd.DataFrame) -> go.Figure:
    top = rules.head(12).copy()
    top["rule"] = top["antecedents"] + " → " + top["consequents"]
    fig = px.bar(
        top, x="lift", y="rule", orientation="h",
        color="confidence",
        color_continuous_scale=["#7C6EFA", "#0EE3B4"],
        title="Top Association Rules by Lift",
        labels={"lift": "Lift", "rule": "Rule", "confidence": "Confidence"},
    )
    fig.update_traces(marker_line_width=0)
    fig.update_layout(**_base_layout(), yaxis={"categoryorder": "total ascending"})
    return fig


def support_confidence_scatter(rules: pd.DataFrame) -> go.Figure:
    fig = px.scatter(
        rules, x="support", y="confidence",
        size="lift", color="lift",
        color_continuous_scale=["#7C6EFA", "#F5C542", "#0EE3B4"],
        title="Support vs Confidence (bubble = Lift)",
        hover_data=["antecedents", "consequents"],
        labels={"support": "Support", "confidence": "Confidence", "lift": "Lift"},
    )
    fig.update_layout(**_base_layout())
    return fig


def itemset_bar(freq: pd.DataFrame) -> go.Figure:
    top = freq.head(12)
    fig = px.bar(
        top, x="support", y="itemsets", orientation="h",
        color="support",
        color_continuous_scale=["#7C6EFA", "#0EE3B4"],
        title="Top Frequent Itemsets by Support",
    )
    fig.update_traces(marker_line_width=0)
    fig.update_layout(
        **_base_layout(),
        yaxis={"categoryorder": "total ascending"},
        coloraxis_showscale=False,
    )
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Anomaly detection charts
# ─────────────────────────────────────────────────────────────────────────────

def anomaly_scatter(df_anom: pd.DataFrame) -> go.Figure:
    normal    = df_anom[~df_anom["is_anomaly"]]
    anomalies = df_anom[df_anom["is_anomaly"]]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=normal.index, y=normal["Purchase"],
        mode="markers",
        name="Normal",
        marker=dict(color="#7C6EFA", size=3.5, opacity=0.45,
                    line=dict(width=0)),
    ))
    fig.add_trace(go.Scatter(
        x=anomalies.index, y=anomalies["Purchase"],
        mode="markers",
        name="Anomaly",
        marker=dict(color="#F5C542", size=9, symbol="star", opacity=0.92,
                    line=dict(color="#FF5370", width=1)),
    ))
    fig.update_layout(
        title="Purchase Anomaly Detection",
        xaxis_title="Transaction Index",
        yaxis_title="Purchase Amount (₹)",
        **_base_layout(),
    )
    return fig


def anomaly_type_pie(df_anom: pd.DataFrame) -> go.Figure:
    counts = _value_counts_df(df_anom["anomaly_type"])
    counts.columns = ["Type", "Count"]
    fig = px.pie(
        counts, names="Type", values="Count",
        color_discrete_sequence=["#7C6EFA", "#F5C542", "#FF5370"],
        title="Anomaly Type Distribution",
        hole=0.55,
    )
    fig.update_traces(
        textinfo="percent+label",
        pull=[0, 0.06, 0],
        marker=dict(line=dict(color="rgba(4,9,20,0.8)", width=2)),
    )
    fig.update_layout(**_base_layout())
    return fig


def zscore_histogram(df_anom: pd.DataFrame) -> go.Figure:
    fig = px.histogram(
        df_anom, x="z_score", nbins=50,
        color_discrete_sequence=["#0EE3B4"],
        title="Z-Score Distribution",
        labels={"z_score": "Z-Score"},
    )
    fig.update_traces(
        marker_line_color="rgba(14,227,180,0.4)",
        marker_line_width=0.5,
        opacity=0.82,
    )
    fig.add_vline(
        x=3, line_dash="dash", line_color="#F5C542",
        annotation_text="Threshold (3σ)",
        annotation_font_color="#F5C542",
        annotation_font_size=11,
    )
    fig.update_layout(**_base_layout())
    return fig