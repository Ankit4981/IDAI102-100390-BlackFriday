"""
╔══════════════════════════════════════════════════════════════════╗
║  Black Friday Intelligence Dashboard  ·  Premium UI v4          ║
║  Bricolage Grotesque · DM Sans · Plotly dark · Custom Logo       ║
╚══════════════════════════════════════════════════════════════════╝
Run:  streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import base64, os
from PIL import Image

from auth        import render_auth_page, is_authenticated, logout
from styles      import inject_css, section_header, page_header, kpi_row, ai_box, info_box
from data_loader import load_data, get_summary
from analytics   import (compute_elbow, run_kmeans, run_apriori,
                          detect_anomalies, generate_insights)
import charts as C

# ── Logo helpers ──────────────────────────────────────────────────
_LOGO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")

def _logo_b64() -> str:
    """Return the logo as a base64 data-URI (cached after first call)."""
    with open(_LOGO_PATH, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()

_LOGO_B64 = _logo_b64() if os.path.exists(_LOGO_PATH) else ""
_LOGO_PIX = Image.open(_LOGO_PATH) if os.path.exists(_LOGO_PATH) else "🛍️"

# ── Page config ───────────────────────────────────────────────────
st.set_page_config(
    page_title="Black Friday AI Dashboard",
    page_icon=_LOGO_PIX,
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

# ── Auth gate ─────────────────────────────────────────────────────
if not is_authenticated():
    render_auth_page()
    st.stop()

# ══════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════
with st.sidebar:

    # ── Brand block ─────────────────────────────────────────────────
    _logo_html = (
        f'<img src="{_LOGO_B64}" style="width:56px;height:56px;border-radius:16px;'
        'box-shadow:0 8px 28px rgba(124,110,250,0.4);">'
        if _LOGO_B64 else '<span style="font-size:26px;">🛍️</span>'
    )
    st.markdown(
        f'<div class="brand-block">'
        f'<div class="brand-icon-wrap" style="background:none;box-shadow:none;">{_logo_html}</div>'
        f'<div class="brand-name">Black Friday AI</div>'
        f'<div class="brand-tag">Intelligence Dashboard · v4</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # ── Analytics nav ────────────────────────────────────────────────
    st.markdown('<span class="nav-label">Analytics</span>', unsafe_allow_html=True)

    NAV_ITEMS = [
        ("🏠", "Dashboard Overview"),
        ("📊", "Exploratory Analysis"),
        ("🎯", "Customer Segmentation"),
        ("🛒", "Market Basket Analysis"),
        ("🚨", "Anomaly Detection"),
        ("💡", "Insights & Recommendations"),
    ]
    UTILITY_ITEMS = [
        ("📥", "Download Reports"),
        ("ℹ️", "About Project"),
    ]

    nav_labels  = [f"{e}  {t}" for e, t in NAV_ITEMS]
    util_labels = [f"{e}  {t}" for e, t in UTILITY_ITEMS]
    all_labels  = nav_labels + util_labels

    if "nav_selection" not in st.session_state:
        st.session_state.nav_selection = all_labels[0]

    nav = st.radio(
        "nav",
        all_labels,
        index=all_labels.index(st.session_state.nav_selection),
        label_visibility="collapsed",
        key="main_nav",
    )
    st.session_state.nav_selection = nav

    # ── Utilities divider ───────────────────────────────────────────
    st.markdown('<div class="nav-divider" style="margin:10px 4px 6px;"></div>', unsafe_allow_html=True)
    st.markdown('<span class="nav-label">Utilities</span>', unsafe_allow_html=True)

    # ── Dataset upload ──────────────────────────────────────────────
    st.markdown('<div class="nav-divider" style="margin-top:10px;"></div>', unsafe_allow_html=True)
    st.markdown('<span class="nav-label">Dataset</span>', unsafe_allow_html=True)

    with st.expander("📂  Upload Dataset"):
        uploaded = st.file_uploader(
            "CSV or Excel",
            type=["csv", "xlsx"],
            key="csv_upload",
            help="Upload your own dataset. BlackFriday.csv in the project folder is auto-detected.",
        )

    # ── User card ───────────────────────────────────────────────────
    st.markdown('<div class="nav-divider" style="margin:14px 4px 10px;"></div>', unsafe_allow_html=True)

    uname   = st.session_state.get("user_name", "Analyst")
    uemail  = st.session_state.get("user_email", "")
    initial = uname[0].upper() if uname else "A"
    st.markdown(
        f'<div class="user-card">'
        f'<div class="user-av">{initial}</div>'
        f'<div>'
        f'<div class="user-name">{uname}</div>'
        f'<div class="user-email">{uemail}</div>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    if st.button("🚪  Sign Out", use_container_width=True):
        for k in ["_df", "_data_source", "_data_key"]:
            st.session_state.pop(k, None)
        logout()
        st.rerun()

    st.markdown(
        '<div style="text-align:center;margin-top:16px;font-size:10px;'
        'color:rgba(86,99,128,0.4);letter-spacing:0.5px;">v4.0 · Data Mining Suite</div>',
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════
# DATA MANAGEMENT — session-state cache to avoid reloads on every
# page switch and to sidestep UploadedFile hashing issues.
# ══════════════════════════════════════════════════════════════════
def _file_key(f):
    """Stable key for an uploaded file (or None)."""
    return (f.name, f.size) if f is not None else None

_cur_key = _file_key(uploaded)
# Load data if: (a) first run — "_df" not yet in session state, OR
#               (b) user swapped the uploaded file
if "_df" not in st.session_state or st.session_state.get("_data_key") != _cur_key:
    with st.spinner("⚡ Loading dataset…"):
        df_raw, data_source = load_data(uploaded)
    st.session_state._df          = df_raw
    st.session_state._data_source = data_source
    st.session_state._data_key    = _cur_key

df_raw      = st.session_state._df
data_source = st.session_state._data_source
summary     = get_summary(df_raw)


# ══════════════════════════════════════════════════════════════════
# PAGE: DASHBOARD OVERVIEW
# ══════════════════════════════════════════════════════════════════
if "Dashboard" in nav:

    page_header(
        "Black Friday Intelligence",
        "Comprehensive data mining & customer behaviour analysis platform",
    )

    # Welcome banner
    st.markdown(
        f'<div class="welcome-banner">'
        f'<div class="welcome-avatar">👋</div>'
        f'<div style="flex:1;">'
        f'<div class="welcome-text-main">Welcome back, {uname}!</div>'
        f'<div class="welcome-text-sub">Dataset active · '
        f'<strong style="color:#0EE3B4;">{data_source}</strong>'
        f' · {summary["rows"]:,} records loaded</div>'
        f'<div class="live-badge"><div class="live-dot"></div>&nbsp;Live Analysis</div>'
        f'</div>'
        f'<div style="text-align:right;opacity:0.55;">'
        f'<div style="font-size:11px;color:#566380;margin-bottom:4px;">QUICK STATS</div>'
        f'<div style="font-size:13px;color:#A0ABBE;">'
        f'📋 {summary["rows"]:,} rows &nbsp;·&nbsp; '
        f'🔢 {summary["columns"]} cols &nbsp;·&nbsp; '
        f'👨 {summary["gender_m_pct"]}% male'
        f'</div></div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # ── Single 4-metric KPI row (primary)
    kpi_row([
        {"icon": "💰", "value": f"₹{summary['total_revenue']/1_000_000:.1f}M",
         "label": "Total Revenue",     "trend": "Black Friday"},
        {"icon": "🛒", "value": f"₹{summary['avg_purchase']:,.0f}",
         "label": "Avg Purchase",      "trend": "per transaction"},
        {"icon": "👤", "value": f"{summary['unique_users']:,}",
         "label": "Unique Customers",  "trend": "active users"},
        {"icon": "📦", "value": f"{summary['unique_products']:,}",
         "label": "Products Sold",     "trend": "across categories"},
    ])
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Secondary stat pills (clean, compact row)
    pct_missing = summary['missing_pct']
    miss_color  = "#FF5370" if pct_missing > 5 else "#0EE3B4"
    st.markdown(
        f'<div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:6px;">'
        f'<div class="stat-pill"><div><div class="stat-pill-val">{summary["rows"]:,}</div>'
        f'<div class="stat-pill-lbl">Total Records</div></div></div>'
        f'<div class="stat-pill"><div><div class="stat-pill-val">{summary["columns"]}</div>'
        f'<div class="stat-pill-lbl">Columns</div></div></div>'
        f'<div class="stat-pill"><div>'
        f'<div class="stat-pill-val" style="color:{miss_color};">{pct_missing}%</div>'
        f'<div class="stat-pill-lbl">Missing Data</div></div></div>'
        f'<div class="stat-pill"><div><div class="stat-pill-val">{summary["gender_m_pct"]}%</div>'
        f'<div class="stat-pill-lbl">Male Customers</div></div></div>'
        f'<div class="stat-pill"><div><div class="stat-pill-val">{summary["unique_products"]:,}</div>'
        f'<div class="stat-pill-lbl">Unique Products</div></div></div>'
        f'</div>',
        unsafe_allow_html=True,
    )
    info_box("Upload your own <strong>BlackFriday.csv</strong> via the sidebar to analyse real data. "
             "Currently running on: <strong>" + data_source + "</strong>.")

    # ── Charts: histogram (wide) + pie (narrow)
    section_header("📈", "Revenue Overview", "High-level performance snapshot")
    c1, c2 = st.columns([5, 3])
    with c1:
        st.plotly_chart(C.purchase_histogram(df_raw), use_container_width=True)
    with c2:
        st.plotly_chart(C.gender_pie(df_raw), use_container_width=True)

    # ── Age revenue + City spend + Occupation scatter in 3 columns
    c3, c4, c5 = st.columns(3)
    with c3:
        st.plotly_chart(C.age_revenue_bar(df_raw), use_container_width=True)
    with c4:
        st.plotly_chart(C.city_spend_bar(df_raw), use_container_width=True)
    with c5:
        st.plotly_chart(C.occupation_scatter(df_raw), use_container_width=True)

    # ── Dataset preview (collapsed by default on overview)
    section_header("🗃️", "Dataset Preview", f"First 100 rows · {data_source}")
    with st.expander("📋  Expand to view raw data", expanded=False):
        st.dataframe(df_raw.head(100), use_container_width=True, height=320)


# ══════════════════════════════════════════════════════════════════
# PAGE: EDA
# ══════════════════════════════════════════════════════════════════
elif "Exploratory" in nav:

    page_header(
        "Exploratory Data Analysis",
        "Interactive charts with real-time demographic filters",
        "Exploratory Analysis",
    )

    # Filter panel
    with st.expander("🎛️  Filters & Controls", expanded=True):
        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            gf = st.multiselect(
                "Gender",
                df_raw["Gender"].unique().tolist(),
                default=df_raw["Gender"].unique().tolist(),
            )
        with fc2:
            age_ord = ["0-17", "18-25", "26-35", "36-45", "46-50", "51-55", "55+"]
            age_opt = [a for a in age_ord if a in df_raw["Age"].unique()]
            af = st.multiselect("Age Group", age_opt, default=age_opt)
        with fc3:
            cf = st.multiselect(
                "City Category",
                df_raw["City_Category"].unique().tolist(),
                default=df_raw["City_Category"].unique().tolist(),
            )

    df_f = df_raw[
        df_raw["Gender"].isin(gf) &
        df_raw["Age"].isin(af) &
        df_raw["City_Category"].isin(cf)
    ]

    if df_f.empty:
        st.warning("No records match the selected filters. Please adjust your selections.")
        st.stop()

    info_box(f"Showing <strong>{len(df_f):,}</strong> of {len(df_raw):,} records after filters. "
             "Charts update in real-time as you adjust the controls above.")

    kpi_row([
        {"icon": "🔍", "value": f"{len(df_f):,}",                       "label": "Filtered Records"},
        {"icon": "💰", "value": f"₹{df_f['Purchase'].mean():,.0f}",      "label": "Avg Purchase"},
        {"icon": "📈", "value": f"₹{df_f['Purchase'].sum()/1e6:.1f}M",   "label": "Total Revenue"},
        {"icon": "📊", "value": f"₹{df_f['Purchase'].median():,.0f}",    "label": "Median Purchase"},
    ])
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "📈  Distributions",
        "🔥  Heatmap & Correlations",
        "📦  Box & Scatter",
        "📋  Statistics",
    ])

    with tab1:
        # Row 1: histogram (wide) + gender pie (narrow)
        r1a, r1b = st.columns([5, 3])
        with r1a: st.plotly_chart(C.purchase_histogram(df_f), use_container_width=True)
        with r1b: st.plotly_chart(C.gender_pie(df_f), use_container_width=True)
        # Row 2: category bar + age revenue + city spend
        r2a, r2b, r2c = st.columns(3)
        with r2a: st.plotly_chart(C.category_bar(df_f), use_container_width=True)
        with r2b: st.plotly_chart(C.age_revenue_bar(df_f), use_container_width=True)
        with r2c: st.plotly_chart(C.city_spend_bar(df_f), use_container_width=True)

    with tab2:
        hm_col, _ = st.columns([3, 1])
        with hm_col:
            st.plotly_chart(C.correlation_heatmap(df_f), use_container_width=True)

    with tab3:
        # Box plot + occupation scatter side by side
        bp_col, sc_col = st.columns(2)
        with bp_col:
            st.plotly_chart(C.purchase_boxplot(df_f), use_container_width=True)
        with sc_col:
            st.plotly_chart(C.occupation_scatter(df_f), use_container_width=True)

    with tab4:
        section_header("📋", "Descriptive Statistics", "Computed on filtered dataset")
        st.dataframe(df_f.describe().T.round(2), use_container_width=True)


# ══════════════════════════════════════════════════════════════════
# PAGE: CUSTOMER SEGMENTATION
# ══════════════════════════════════════════════════════════════════
elif "Segmentation" in nav:

    page_header(
        "Customer Segmentation",
        "K-Means clustering — identify Budget, Average & Premium buyer profiles",
        "Customer Segmentation",
    )

    with st.expander("⚙️  Clustering Configuration", expanded=True):
        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            n_clusters = st.slider(
                "Number of Clusters (k)", 2, 7, 3,
                help="Optimal k typically between 3–5",
            )
        with sc2:
            show_elbow = st.checkbox("Show Elbow Curve", value=True)
        with sc3:
            st.markdown("<br>", unsafe_allow_html=True)
            st.info("Features: **Age + Occupation + Purchase**")

    if show_elbow:
        section_header("📐", "Elbow Method", "Find the optimal number of clusters")
        with st.spinner("Computing within-cluster inertia…"):
            inertias = compute_elbow(df_raw)
        st.plotly_chart(C.elbow_chart(inertias), use_container_width=True)

    section_header("🎯", "Clustering Results", f"k = {n_clusters} clusters")
    with st.spinner(f"Running K-Means (k={n_clusters})…"):
        df_cl = run_kmeans(df_raw, n_clusters)

    cl_summary = (
        df_cl.groupby("cluster_label")["Purchase"]
        .agg(["mean", "count", "sum"])
        .reset_index()
    )
    kpi_row([
        {"icon": "🎯",
         "value": f"₹{row['mean']:,.0f}",
         "label": f"{row['cluster_label']} · {int(row['count']):,} users"}
        for _, row in cl_summary.iterrows()
    ])
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # ── Charts: scatter + dist side by side, box spans full width
    ch1, ch2 = st.columns([3, 2])
    with ch1: st.plotly_chart(C.cluster_scatter(df_cl), use_container_width=True)
    with ch2: st.plotly_chart(C.cluster_dist(df_cl), use_container_width=True)
    st.plotly_chart(C.cluster_box(df_cl), use_container_width=True)

    # ── Cluster profiles in 2 columns
    section_header("📋", "Cluster Profiles", "AI-generated segment descriptions")

    # Split clusters into two columns
    profile_rows = list(cl_summary.iterrows())
    left_rows  = profile_rows[::2]          # even indices → left col
    right_rows = profile_rows[1::2]         # odd  indices → right col

    def _cluster_color(lbl: str) -> str:
        if "Budget"  in lbl: return "#7C6EFA"
        if "Premium" in lbl or "Elite" in lbl or "VIP" in lbl or "Diamond" in lbl: return "#F5C542"
        return "#0EE3B4"

    def _cluster_tip(lbl: str, avg: float) -> str:
        if "Budget" in lbl:
            return (f"Price-sensitive segment averaging ₹{avg:,.0f}. "
                    "Target with flash sales, coupon drops, and value bundles "
                    "to maximise conversion at lower ticket sizes.")
        if "Premium" in lbl or "Elite" in lbl or "VIP" in lbl or "Diamond" in lbl:
            return (f"High-value VIP segment at ₹{avg:,.0f} average. "
                    "Invest in loyalty tiers, exclusive early-access deals, "
                    "and personalised upsell journeys to maximise LTV.")
        return (f"Core mid-market segment at ₹{avg:,.0f}. "
                "Upsell premium bundles and cross-category promotions "
                "to graduate them toward higher spending tiers.")

    def _render_cluster_card(row_data):
        mean_p = row_data["mean"]
        label  = row_data["cluster_label"]
        cnt    = int(row_data["count"])
        color  = _cluster_color(label)
        tip    = _cluster_tip(label, mean_p)
        pct    = round(cnt / len(df_cl) * 100, 1)
        st.markdown(
            f'<div class="insight-card" style="border-left-color:{color};">'
            f'<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;">'
            f'<div style="font-family:\'Bricolage Grotesque\',sans-serif;font-size:15px;'
            f'font-weight:700;color:{color};">{label}</div>'
            f'<div style="text-align:right;">'
            f'<div style="font-size:13px;color:#EDF2F7;font-weight:600;">₹{mean_p:,.0f}</div>'
            f'<div style="font-size:10px;color:#566380;margin-top:2px;">{cnt:,} users · {pct}%</div>'
            f'</div></div>'
            f'<div class="insight-card-text">{tip}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    pc1, pc2 = st.columns(2)
    with pc1:
        for _, r in left_rows:  _render_cluster_card(r)
    with pc2:
        for _, r in right_rows: _render_cluster_card(r)


# ══════════════════════════════════════════════════════════════════
# PAGE: MARKET BASKET ANALYSIS
# ══════════════════════════════════════════════════════════════════
elif "Market Basket" in nav:

    page_header(
        "Market Basket Analysis",
        "Apriori algorithm — frequent itemsets & association rule mining",
        "Market Basket Analysis",
    )

    with st.expander("⚙️  Apriori Configuration", expanded=True):
        mc1, mc2 = st.columns(2)
        with mc1:
            min_sup = st.slider(
                "Minimum Support", 0.005, 0.15, 0.02, 0.005,
                format="%.3f",
                help="Fraction of transactions containing the itemset",
            )
        with mc2:
            min_conf = st.slider(
                "Minimum Confidence", 0.10, 0.90, 0.30, 0.05,
                format="%.2f",
                help="P(B | A) — probability of B given A is purchased",
            )

    with st.spinner("Mining frequent itemsets and association rules…"):
        freq_items, rules = run_apriori(df_raw, min_sup, min_conf)

    max_lift = f"{rules['lift'].max():.2f}" if len(rules) > 0 else "N/A"
    max_conf = f"{rules['confidence'].max():.1%}" if len(rules) > 0 else "N/A"

    kpi_row([
        {"icon": "📋", "value": str(len(freq_items)), "label": "Frequent Itemsets"},
        {"icon": "🔗", "value": str(len(rules)),      "label": "Association Rules"},
        {"icon": "📈", "value": max_lift,              "label": "Max Lift"},
        {"icon": "🎯", "value": max_conf,              "label": "Max Confidence"},
    ])
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs([
        "📊  Visualisations",
        "📋  Itemsets",
        "🔗  Rules Table",
    ])

    with tab1:
        if len(rules) > 0:
            # Rules bar + scatter side by side
            rb_col, sc_col = st.columns(2)
            with rb_col:
                st.plotly_chart(C.rules_bar(rules), use_container_width=True)
            with sc_col:
                st.plotly_chart(C.support_confidence_scatter(rules), use_container_width=True)
        # Itemset bar spans full width
        st.plotly_chart(C.itemset_bar(freq_items), use_container_width=True)

    with tab2:
        st.dataframe(freq_items.reset_index(drop=True), use_container_width=True, height=360)

    with tab3:
        if len(rules) > 0:
            disp = rules[["antecedents", "consequents", "support", "confidence", "lift"]].copy()
            for col_ in ["support", "confidence", "lift"]:
                disp[col_] = disp[col_].map("{:.4f}".format)
            st.dataframe(disp.reset_index(drop=True), use_container_width=True, height=360)
        else:
            st.warning("No rules at current thresholds. Try reducing support or confidence.")

    section_header("🤖", "Rule Interpretation")
    ai_box(
        "Association rules reveal product combinations bought together. "
        "A <strong>Lift &gt; 1</strong> signals a genuine positive association beyond random chance. "
        "High-<strong>confidence</strong> rules reliably predict the consequent item. "
        "Use these patterns to design cross-sell bundles, personalised recommendations, "
        "and product placement strategies for your Black Friday campaign."
    )


# ══════════════════════════════════════════════════════════════════
# PAGE: ANOMALY DETECTION
# ══════════════════════════════════════════════════════════════════
elif "Anomaly" in nav:

    page_header(
        "Anomaly Detection",
        "Statistical outlier analysis — flag high spenders & suspicious transactions",
        "Anomaly Detection",
    )

    with st.expander("⚙️  Detection Settings", expanded=True):
        ac1, ac2 = st.columns(2)
        with ac1:
            method = st.selectbox(
                "Detection Method", ["IQR", "Z-Score"],
                help="IQR = interquartile range fence · Z-Score = standard deviations from mean",
            )
        with ac2:
            threshold = st.slider(
                "Z-Score Threshold", 1.5, 5.0, 3.0, 0.1,
                disabled=(method == "IQR"),
                help="Only used for Z-Score method (3σ is standard)",
            )

    with st.spinner("Detecting anomalies…"):
        df_an = detect_anomalies(df_raw, method, threshold)

    n_anom = int(df_an["is_anomaly"].sum())
    n_high = int((df_an["anomaly_type"] == "High Spender").sum())
    n_low  = int((df_an["anomaly_type"] == "Suspicious Low").sum())

    kpi_row([
        {"icon": "🔍", "value": f"{n_anom:,}",                               "label": "Total Anomalies"},
        {"icon": "💸", "value": f"{n_high:,}",                               "label": "High Spenders"},
        {"icon": "⚠️", "value": f"{n_low:,}",                                "label": "Suspicious Lows"},
        {"icon": "📊", "value": f"{n_anom/max(len(df_an),1)*100:.2f}%",      "label": "Anomaly Rate"},
    ])
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # ── Row 1: scatter (wide) + type pie (narrow)
    ch1, ch2 = st.columns([5, 3])
    with ch1: st.plotly_chart(C.anomaly_scatter(df_an), use_container_width=True)
    with ch2: st.plotly_chart(C.anomaly_type_pie(df_an), use_container_width=True)

    # ── Row 2: Z-score histogram + top anomalies table side by side
    section_header("📋", "Distribution & Top Anomalous Transactions")
    hz_col, tbl_col = st.columns([2, 3])
    with hz_col:
        st.plotly_chart(C.zscore_histogram(df_an), use_container_width=True)
    with tbl_col:
        top_an    = df_an[df_an["is_anomaly"]].sort_values("Purchase", ascending=False).head(20)
        show_cols = [c for c in ["User_ID", "Product_ID", "Gender", "Age",
                                  "Purchase", "anomaly_type", "z_score"] if c in top_an.columns]
        st.dataframe(top_an[show_cols].reset_index(drop=True), use_container_width=True, height=340)

    section_header("🤖", "Anomaly Interpretation")
    ai_box(
        "<strong>High Spenders</strong> represent VIP customers, bulk buyers, or corporate accounts "
        "— prime candidates for loyalty programmes and personalised concierge experiences. "
        "<strong>Suspicious Low</strong> transactions may indicate partial orders, returns, "
        "or data quality issues requiring manual review. "
        "Segment anomalous users into dedicated outreach workflows to maximise revenue impact."
    )


# ══════════════════════════════════════════════════════════════════
# PAGE: INSIGHTS & RECOMMENDATIONS
# ══════════════════════════════════════════════════════════════════
elif "Insights" in nav:

    page_header(
        "AI-Powered Insights",
        "Data-driven business intelligence & actionable recommendations",
        "Insights & Recommendations",
    )

    # generate_insights is now @st.cache_data — instant on repeat visits
    insights = generate_insights(df_raw)

    kpi_row([
        {"icon": "📈", "value": f"₹{insights['avg_purchase']:,.0f}", "label": "Avg Purchase"},
        {"icon": "🏆", "value": insights["top_age"],                 "label": "Top Age Group"},
        {"icon": "🏙️", "value": f"City {insights['top_city']}",      "label": "Highest Spend City"},
        {"icon": "📦", "value": f"Cat {insights['top_category']}",   "label": "Top Category"},
    ])
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # Key findings
    section_header("🔍", "Key Findings", "Auto-generated from dataset patterns")
    ic1, ic2 = st.columns(2)

    cards_left = [
        ("👥 Age Group Analysis",
         f"The <strong style='color:#0EE3B4'>{insights['top_age']}</strong> cohort leads "
         f"with avg spend of <strong style='color:#F5C542'>₹{insights['top_age_spend']:,}</strong>. "
         "Campaigns targeting this demographic yield the highest revenue per impression."),
        ("⚡ Gender Spending Gap",
         f"{insights['gender_insight']} "
         f"Male avg: <strong style='color:#B8ACFF'>₹{insights['gender_male']:,}</strong> · "
         f"Female avg: <strong style='color:#0EE3B4'>₹{insights['gender_female']:,}</strong>."),
        ("🏙️ City Performance",
         f"City <strong style='color:#0EE3B4'>{insights['top_city']}</strong> drives "
         f"<strong style='color:#F5C542'>₹{insights['top_city_spend']:,}</strong> avg spend. "
         "Prioritise inventory placement and ad spend in this market."),
    ]
    cards_right = [
        ("📦 Category Leadership",
         f"Product Category <strong style='color:#0EE3B4'>{insights['top_category']}</strong> "
         f"leads with <strong style='color:#F5C542'>{insights['top_cat_count']:,}</strong> "
         "purchases. Ensure homepage placement and deep discounting for this category."),
        ("💎 VIP Spending Tier",
         f"Top 10% of customers spend above "
         f"<strong style='color:#F5C542'>₹{insights['high_value_threshold']:,}</strong>. "
         "Design exclusive bundles and early-access events for this premium tier."),
        ("📊 Revenue Snapshot",
         f"Dataset total revenue: <strong style='color:#F5C542'>₹{insights['total_revenue']:,}</strong> "
         f"across <strong style='color:#0EE3B4'>{len(df_raw):,}</strong> transactions. "
         f"Average basket: ₹{insights['avg_purchase']:,.0f}."),
    ]

    with ic1:
        for title, text in cards_left:
            st.markdown(f"""
            <div class="insight-card">
              <div class="insight-card-title">{title}</div>
              <div class="insight-card-text">{text}</div>
            </div>
            """, unsafe_allow_html=True)

    with ic2:
        for title, text in cards_right:
            st.markdown(f"""
            <div class="insight-card">
              <div class="insight-card-title">{title}</div>
              <div class="insight-card-text">{text}</div>
            </div>
            """, unsafe_allow_html=True)

    # Strategic recommendations
    section_header("🚀", "Strategic Recommendations", "Data-backed action plan")
    recs = [
        ("🎯", "Precision Targeting",
         f"Focus ads on the {insights['top_age']} age group in City {insights['top_city']} "
         f"using Category {insights['top_category']} as the hero SKU. Expected 15–25% higher CTR."),
        ("💳", "VIP Loyalty Tier",
         f"Enrol customers spending above ₹{insights['high_value_threshold']:,} "
         "in a dedicated VIP programme with exclusive discounts and priority shipping."),
        ("🔄", "Cross-Sell Bundles",
         "Association rules reveal frequent multi-category co-purchases. "
         "Bundle complementary products to increase average order value by an estimated 18%."),
        ("📱", "Mobile-First Creatives",
         "Male customers (75%+) skew toward tech & electronics. "
         "Design mobile-first video ads featuring top-category products."),
        ("🏪", "City Inventory Optimisation",
         f"City {insights['top_city']} shows peak spend — pre-position premium inventory "
         "and reduce stockout risk to prevent lost sales on Black Friday day."),
        ("⚡", "Flash Sale Timing",
         "Anomaly spikes indicate time-clustered purchase surges. "
         "Schedule hourly flash deals during identified peak windows to maximise urgency-driven revenue."),
    ]
    # 3-column recommendation grid
    rc1, rc2, rc3 = st.columns(3)
    cols_cycle = [rc1, rc2, rc3]
    for i, (icon, title, text) in enumerate(recs):
        with cols_cycle[i % 3]:
            st.markdown(
                f'<div class="insight-card">'
                f'<div style="font-size:22px;margin-bottom:8px;">{icon}</div>'
                f'<div class="insight-card-title">{title}</div>'
                f'<div class="insight-card-text">{text}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )


# ══════════════════════════════════════════════════════════════════
# PAGE: DOWNLOAD REPORTS
# ══════════════════════════════════════════════════════════════════
elif "Download" in nav:

    page_header(
        "Download Reports",
        "Export datasets, analysis results, and executive summaries",
        "Download Reports",
    )

    section_header("📁", "Available Exports")

    def dl_card(icon, title, desc, btn_label, data, fname, mime):
        st.markdown(f"""
        <div class="dl-card">
          <div class="dl-icon">{icon}</div>
          <div class="dl-title">{title}</div>
          <div class="dl-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)
        st.download_button(
            btn_label, data=data, file_name=fname,
            mime=mime, use_container_width=True,
        )

    row1 = st.columns(3)
    with row1[0]:
        dl_card(
            "📄", "Full Dataset", "Complete cleaned dataset with all features",
            "⬇️  Dataset CSV",
            df_raw.to_csv(index=False).encode(),
            "blackfriday_dataset.csv", "text/csv",
        )
    with row1[1]:
        dl_card(
            "📊", "Descriptive Stats", "Numeric summary of all columns",
            "⬇️  Statistics CSV",
            df_raw.describe().T.round(3).to_csv().encode(),
            "blackfriday_stats.csv", "text/csv",
        )
    with row1[2]:
        # Re-use cached K-Means result (k=3 default)
        df_cl2 = run_kmeans(df_raw, 3)
        keep   = [c for c in ["User_ID", "Purchase", "cluster_label", "cluster_id"]
                  if c in df_cl2.columns]
        dl_card(
            "🎯", "Cluster Results", "Customer segmentation labels",
            "⬇️  Clusters CSV",
            df_cl2[keep].to_csv(index=False).encode(),
            "blackfriday_clusters.csv", "text/csv",
        )

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
    row2 = st.columns(3)

    with row2[0]:
        # Re-use default IQR anomaly result (cached)
        df_an2 = detect_anomalies(df_raw)
        ac     = [c for c in ["Purchase", "is_anomaly", "anomaly_type", "z_score"]
                  if c in df_an2.columns]
        dl_card(
            "🚨", "Anomaly Results", "Flagged transactions with scores",
            "⬇️  Anomalies CSV",
            df_an2[ac].to_csv(index=False).encode(),
            "blackfriday_anomalies.csv", "text/csv",
        )

    with row2[1]:
        ins2   = generate_insights(df_raw)   # cached — free
        report = f"""BLACK FRIDAY INTELLIGENCE DASHBOARD — EXECUTIVE REPORT
{"=" * 62}
Dataset : {data_source}
Analyst : {st.session_state.get('user_name', 'Analyst')}
Records : {summary['rows']:,}

PURCHASE STATISTICS
  Total Revenue  : ₹{ins2['total_revenue']:,}
  Average Basket : ₹{ins2['avg_purchase']:,.2f}
  VIP Threshold  : ₹{ins2['high_value_threshold']:,}+

DEMOGRAPHIC INSIGHTS
  Top Age Group  : {ins2['top_age']} (avg ₹{ins2['top_age_spend']:,})
  Male Avg       : ₹{ins2['gender_male']:,}
  Female Avg     : ₹{ins2['gender_female']:,}
  Top City       : City {ins2['top_city']} (avg ₹{ins2['top_city_spend']:,})
  Top Category   : Category {ins2['top_category']}

RECOMMENDATIONS
  1. Target {ins2['top_age']} cohort in City {ins2['top_city']}
  2. VIP tier for customers > ₹{ins2['high_value_threshold']:,}
  3. Feature Category {ins2['top_category']} as hero SKU
  4. Deploy cross-sell bundles from association rules
  5. Flash sales during anomaly-detected peak windows
{"=" * 62}
"""
        dl_card(
            "📝", "Executive Summary", "Full text intelligence report",
            "⬇️  Report TXT",
            report.encode(), "blackfriday_report.txt", "text/plain",
        )

    with row2[2]:
        dl_card(
            "📈", "Association Rules", "Frequent itemsets + rules",
            "⬇️  Rules CSV",
            pd.DataFrame({"info": ["Run Market Basket Analysis page first"]})
            .to_csv(index=False).encode(),
            "blackfriday_rules.csv", "text/csv",
        )


# ══════════════════════════════════════════════════════════════════
# PAGE: ABOUT
# ══════════════════════════════════════════════════════════════════
elif "About" in nav:

    _hero_logo = (
        f'<img src="{_LOGO_B64}" style="width:72px;height:72px;border-radius:20px;'
        'box-shadow:0 12px 36px rgba(124,110,250,0.5);display:block;margin:0 auto 20px;">'
        if _LOGO_B64
        else '<div style="width:72px;height:72px;border-radius:20px;margin:0 auto 20px;'
             'background:linear-gradient(135deg,#7C6EFA,#0EE3B4);display:flex;'
             'align-items:center;justify-content:center;font-size:34px;'
             'box-shadow:0 12px 36px rgba(124,110,250,0.45);">\U0001f6cd\ufe0f</div>'
    )
    st.markdown(
        f'<div class="about-hero">'
        f'{_hero_logo}'
        f'<div class="page-title" style="font-size:36px;margin-bottom:12px;">Black Friday AI Dashboard</div>'
        f'<div style="font-size:14px;color:#A0ABBE;max-width:580px;margin:0 auto;line-height:1.75;">'
        f'A premium production-level data mining application delivering deep customer behaviour '
        f'insights through advanced machine learning, statistical analysis, and interactive '
        f'data visualisation.'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    section_header("🔧", "Feature Modules")
    mods = [
        ("📊", "EDA Module",          "8+ interactive Plotly charts with real-time demographic filters"),
        ("🎯", "K-Means Clustering",  "Elbow optimisation, cluster labelling, profile analysis"),
        ("🛒", "Apriori Mining",      "Frequent itemsets, association rules with support/confidence/lift"),
        ("🚨", "Anomaly Detection",   "IQR & Z-Score with visual scatter + pie + histogram"),
        ("💡", "AI Insight Engine",   "Auto-generated patterns with 6 strategic recommendations"),
        ("📥", "Report Exports",      "CSV dataset, stats, clusters, anomalies, TXT summary"),
        ("🔐", "Auth System",         "SHA-256 hashing, signup/login, session management"),
        ("🎨", "Premium UI",          "Glassmorphism, Space Grotesk, animated gradients, dark theme"),
    ]
    m_cols = st.columns(4)
    for i, (icon, title, desc) in enumerate(mods):
        with m_cols[i % 4]:
            st.markdown(
                f'<div class="glass-card" style="min-height:148px;text-align:center;padding:24px 16px;">'
                f'<div style="font-size:30px;margin-bottom:12px;">{icon}</div>'
                f'<div style="font-family:\'Bricolage Grotesque\',sans-serif;font-size:14px;'
                f'font-weight:700;color:#EDF2F7;margin-bottom:8px;letter-spacing:-0.2px;">{title}</div>'
                f'<div style="font-size:12px;color:#566380;line-height:1.6;">{desc}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    section_header("🛠️", "Tech Stack")
    techs = [
        ("🖥️ Frontend",     "Streamlit · Custom CSS Glassmorphism"),
        ("📊 Visualisation","Plotly Express · Graph Objects"),
        ("🤖 ML",           "Scikit-learn (KMeans) · mlxtend (Apriori) · SciPy (Z-Score)"),
        ("🔢 Data",         "Pandas · NumPy"),
        ("🔐 Auth",         "SHA-256 · JSON store · Streamlit session state"),
        ("🎨 Design",       "Space Grotesk · Inter · CSS animations"),
    ]
    tc1, tc2 = st.columns(2)
    for i, (k, v) in enumerate(techs):
        with (tc1 if i % 2 == 0 else tc2):
            st.markdown(
                f'<div class="glass-card" style="padding:14px 18px;margin-bottom:10px;'
                f'display:flex;gap:16px;align-items:center;">'
                f'<div style="font-weight:700;color:#0EE3B4;min-width:150px;font-size:13px;">{k}</div>'
                f'<div style="color:#A0ABBE;font-size:13px;">{v}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div class="glass-card" style="text-align:center;margin-top:24px;padding:22px;">'
        '<div style="color:#566380;font-size:13px;">'
        'Built for academic excellence · Data Mining &amp; Business Intelligence · IDAI102'
        '</div>'
        '<div style="font-size:13px;margin-top:10px;letter-spacing:4px;">'
        '<span style="color:#7C6EFA;">●</span>'
        '<span style="color:#0EE3B4;margin-left:8px;">●</span>'
        '<span style="color:#F5C542;margin-left:8px;">●</span>'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )