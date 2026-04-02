<div align="center">

<img src="logo.png" width="110" style="border-radius: 24px;" alt="Black Friday AI Logo"/>

# ⬛ Black Friday AI Dashboard

### *Intelligence · Data Mining · Machine Learning*

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Streamlit-7C6EFA?style=for-the-badge&logo=streamlit&logoColor=white)](https://blackfriday9171.streamlit.app/)
[![GitHub](https://img.shields.io/badge/Source_Code-GitHub-0EE3B4?style=for-the-badge&logo=github&logoColor=black)](https://github.com/Ankit4981/IDAI102-100390-BlackFriday)
[![Drive](https://img.shields.io/badge/Assets_&_Reports-Google_Drive-F5C542?style=for-the-badge&logo=googledrive&logoColor=black)](https://drive.google.com/drive/folders/1w5GZmtaQzhZGNBo7vK8M8-FJNS8jsQEI?usp=sharing)

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Plotly](https://img.shields.io/badge/Plotly-5.18+-3F4F75?style=flat-square&logo=plotly&logoColor=white)](https://plotly.com)
[![scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3+-F7931E?style=flat-square&logo=scikitlearn&logoColor=white)](https://scikit-learn.org)

---

*A production-grade data mining & customer intelligence platform built for the Kaggle Black Friday dataset — featuring glassmorphism UI, advanced ML analytics, and interactive visualisations.*

</div>

---

## ✦ What Is This?

**Black Friday AI Dashboard** is a full-stack data analytics application that transforms 550 000+ Black Friday retail transactions into actionable business intelligence. It combines a premium dark-mode UI with real machine learning — clustering, association rules, and anomaly detection — all running live in the browser.

> 🎯 **Demo credentials** → `demo@blackfriday.ai` / `demo123`

---

## 🖥️ Screenshots

> *Open the live app to experience the full animated interface.*

| Login Screen | Dashboard Overview |
|:---:|:---:|
| Glassmorphism auth with animated dot grid | KPI cards + revenue charts |

| Customer Segmentation | Market Basket Analysis |
|:---:|:---:|
| K-Means elbow + cluster scatter | Apriori itemsets + association rules |

---

## ⚡ Feature Modules

### 🏠 Dashboard Overview
- **6 live KPI cards** — total revenue, avg basket, unique users, products, missing data %, male/female split
- Welcome banner with active dataset label and row count
- Dataset source badge (real CSV, uploaded file, or synthetic fallback)

### 📊 Exploratory Data Analysis
8 interactive Plotly charts with real-time demographic filters:

| Chart | Type | Insight |
|---|---|---|
| Purchase Distribution | Histogram + mean line | Spend skew & outlier shape |
| Purchase by Age Group | Box plot | Median & IQR per cohort |
| Product Category Popularity | Bar + colour scale | Top 15 SKU categories |
| Gender Distribution | Donut pie | M/F purchase split |
| City Category Revenue | Grouped bar + labels | A/B/C city performance |
| Feature Correlation Matrix | Heatmap | Inter-variable relationships |
| Revenue by Age Group | Stacked bar | Which cohort drives revenue |
| Avg Purchase by Occupation | Bubble scatter | Occupation spend profile |

Sidebar filters: **Gender · Age group · City · Date range · Purchase range slider**

### 🎯 Customer Segmentation (K-Means)
- **Elbow method chart** to determine optimal *k* (up to k=10)
- Configurable cluster count (2–7) via slider
- Auto-ranked cluster labels: 💰 Budget → 💎 Diamond Buyers
- Cluster scatter, distribution bar, and purchase box-plot
- Per-cluster **profile cards** with demographics breakdown
- Encoded features: Age (numeric), Occupation, Purchase — scaled with `StandardScaler`

### 🛒 Market Basket Analysis (Apriori)
- Uses `mlxtend` with graceful fallback to co-occurrence analysis
- Configurable **minimum support** and **minimum confidence** sliders
- **3 output charts**: Top rules by lift (horizontal bar), Support vs Confidence bubble scatter, Frequent itemsets bar
- Rules table with antecedents → consequents, support, confidence, lift
- Basket construction per `User_ID` on `Product_Category_1`

### 🚨 Anomaly Detection
- Two detection methods: **IQR** (interquartile range) and **Z-Score** (configurable threshold σ)
- Anomaly classification: `Normal` / `High Spender` / `Suspicious Low`
- **3 charts**: Purchase scatter with star markers on anomalies, anomaly type donut pie, Z-score histogram with 3σ threshold line
- Summary table of top anomalous transactions

### 💡 AI Insights & Recommendations
- Auto-generated insight cards covering: top spending age group, gender gap, most popular category, top city, revenue totals
- **6 strategic recommendations** tied directly to the data
- Highlighted metric callouts with trend icons

### 📥 Download Reports
6 one-click exports:
- `blackfriday_dataset.csv` — full cleaned dataset
- `blackfriday_stats.csv` — descriptive statistics
- `blackfriday_clusters.csv` — segmentation labels per user
- `blackfriday_anomalies.csv` — flagged transactions with Z-scores
- `blackfriday_rules.csv` — association rules
- `blackfriday_report.txt` — executive summary text report

### 🔐 Authentication System
- Signup / Login with **SHA-256 password hashing**
- JSON-based user store (`users.json`)
- Streamlit session state for persistent login
- Glassmorphism auth card with animated gradient and logo

---

## 🛠️ Tech Stack

```
┌─────────────────────────────────────────────────────────┐
│  FRONTEND        Streamlit · Custom CSS Glassmorphism   │
│  VISUALISATION   Plotly Express · Plotly Graph Objects  │
│  MACHINE LEARNING                                       │
│    Clustering    Scikit-learn  →  KMeans + StandardScaler│
│    Assoc. Rules  mlxtend       →  Apriori + assoc_rules │
│    Anomalies     SciPy         →  Z-Score / IQR         │
│  DATA LAYER      Pandas · NumPy                         │
│  AUTH            hashlib SHA-256 · JSON · session_state │
│  FONTS           Bricolage Grotesque · DM Sans          │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
BlackFriday/
│
├── app.py               # Main Streamlit entry point
├── auth.py              # Authentication UI & logic
├── analytics.py         # ML computations (clustering, Apriori, anomalies)
├── charts.py            # All Plotly chart functions
├── data_loader.py       # CSV loading, cleaning & synthetic fallback
├── styles.py            # CSS injection & reusable UI components
│
├── BlackFriday.csv      # Kaggle dataset (550K+ rows)
├── logo.png             # App logo
├── users.json           # Auth store (auto-created)
└── requirements.txt     # Python dependencies
```

---

## 🚀 Local Setup

```bash
# 1 — Clone the repository
git clone https://github.com/Ankit4981/IDAI102-100390-BlackFriday.git
cd IDAI102-100390-BlackFriday

# 2 — Install dependencies
pip install -r requirements.txt

# 3 — Place the dataset
# Download BlackFriday.csv from Kaggle and put it in the project root
# Or let the app generate 10K synthetic rows automatically

# 4 — Launch
streamlit run app.py
```

The app auto-detects `BlackFriday.csv` in the same folder. If absent, it generates a realistic 10 000-row synthetic dataset so you can explore every feature immediately.

---

## 📦 Requirements

```
streamlit>=1.32.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.18.0
scikit-learn>=1.3.0
scipy>=1.11.0
mlxtend>=0.23.0
openpyxl>=3.1.0
```

---

## 📊 Dataset

**Source:** [Kaggle — Black Friday Sales](https://www.kaggle.com/datasets/mehdidag/black-friday)

| Column | Description |
|---|---|
| `User_ID` | Unique customer identifier |
| `Product_ID` | Product SKU code |
| `Gender` | M / F |
| `Age` | Age bucket (0-17, 18-25, …, 55+) |
| `Occupation` | Occupation code (0–20) |
| `City_Category` | City tier — A, B, or C |
| `Stay_In_Current_City_Years` | Years at current city |
| `Marital_Status` | 0 = single, 1 = married |
| `Product_Category_1/2/3` | Product category codes |
| `Purchase` | Purchase amount in ₹ |

---

## 🧠 ML Methodology

### K-Means Clustering
Features are standardised with `StandardScaler` before fitting. After clustering, segments are re-ranked by mean purchase so labels are always semantically consistent (Budget → Diamond), regardless of random initialisation.

### Apriori Association Rules
Baskets are constructed per `User_ID` on `Product_Category_1`. The algorithm returns frequent itemsets and rules filtered by minimum support and confidence. Lift is used as the primary ranking metric — values above 1.0 indicate genuine co-purchase affinity.

### Anomaly Detection
- **IQR method:** flags transactions below `Q1 − 1.5×IQR` or above `Q3 + 1.5×IQR`
- **Z-Score method:** flags transactions where `|z| > threshold` (default 3σ)
- Both methods also compute Z-scores for visualisation, even when IQR is the detection method.

---

## 🎨 UI Design Highlights

- **Glassmorphism cards** with `backdrop-filter: blur(28px)` and layered transparency
- **Animated dot-grid background** on the auth page
- **Gradient accent lines** on every card's top edge (`#7C6EFA → #0EE3B4`)
- **Floating icon animation** on login (`iconFloat` keyframe)
- **Slide-up card entrance** animation (`cubic-bezier(0.22, 1, 0.36, 1)`)
- Fully dark theme — `#040A14` base with purple/teal accent palette
- Responsive 4-column module grid on the About page

---

## 📌 Academic Context

```
Course   : IDAI102 — Artificial Intelligence & Data Mining
Module   : Customer Analytics & Retail Intelligence
Dataset  : Kaggle Black Friday Sales
Approach : EDA → Clustering → Association Rules → Anomaly Detection
```

---

<div align="center">

**Built with 💜 using Python, Streamlit, and ML**

[![Live App](https://img.shields.io/badge/Try_It_Live-blackfriday9171.streamlit.app-7C6EFA?style=for-the-badge)](https://blackfriday9171.streamlit.app/)

*Black Friday AI Dashboard · v4.0 · Data Mining Suite*

</div>
