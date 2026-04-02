"""
Premium CSS Theme v4 — Black Friday Intelligence Dashboard
Redesigned: Refined dark theme · Sharp typography · Elevated components
"""
import streamlit as st

MAIN_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,300;12..96,400;12..96,500;12..96,600;12..96,700;12..96,800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  /* Core palette */
  --primary:        #7C6EFA;
  --primary-dim:    rgba(124,110,250,0.18);
  --primary-glow:   rgba(124,110,250,0.32);
  --secondary:      #0EE3B4;
  --secondary-dim:  rgba(14,227,180,0.14);
  --accent:         #F5C542;
  --danger:         #FF5370;

  /* Backgrounds */
  --bg:             #040A14;
  --bg-2:           #07101E;
  --bg-3:           #0B1828;
  --card:           rgba(11,24,40,0.85);
  --card-hover:     rgba(15,30,50,0.92);

  /* Borders */
  --border:         rgba(124,110,250,0.13);
  --border-bright:  rgba(124,110,250,0.42);
  --border-subtle:  rgba(255,255,255,0.05);

  /* Text */
  --text:           #EDF2F7;
  --text-soft:      #A0ABBE;
  --text-muted:     #566380;

  /* Geometry */
  --radius:         14px;
  --radius-sm:      8px;
  --radius-lg:      20px;

  /* Motion */
  --ease:           cubic-bezier(0.22, 1, 0.36, 1);
  --ease-back:      cubic-bezier(0.34, 1.56, 0.64, 1);
}

/* ─── Global reset ─────────────────────────────────────────── */
html, body, [class*="css"] {
  font-family: 'DM Sans', sans-serif !important;
  color: var(--text) !important;
  -webkit-font-smoothing: antialiased !important;
  -moz-osx-font-smoothing: grayscale !important;
}

/* ─── App background ────────────────────────────────────────── */
.stApp {
  background: var(--bg) !important;
  background-image:
    radial-gradient(ellipse 90% 55% at 20% -8%, rgba(124,110,250,0.11) 0%, transparent 55%),
    radial-gradient(ellipse 65% 45% at 80% 110%, rgba(14,227,180,0.07) 0%, transparent 50%) !important;
  min-height: 100vh !important;
}

/* Subtle dot grid */
.stApp::before {
  content: '';
  position: fixed; inset: 0;
  background-image: radial-gradient(circle, rgba(124,110,250,0.07) 1px, transparent 1px);
  background-size: 28px 28px;
  pointer-events: none; z-index: 0;
}

/* Hide chrome */
#MainMenu, footer, header { visibility: hidden !important; }
.block-container {
  padding: 1.8rem 2.4rem 5rem 2.4rem !important;
  max-width: 1400px !important;
}

/* ═══════════════════════════════════════════════════════════
   SIDEBAR
═══════════════════════════════════════════════════════════ */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #060e1c 0%, #04090f 100%) !important;
  border-right: 1px solid rgba(124,110,250,0.1) !important;
  box-shadow: 8px 0 48px rgba(0,0,0,0.6) !important;
}

[data-testid="stSidebarContent"] {
  padding: 0 14px 24px !important;
}

/* ── Radio nav overrides ── */
[data-testid="stSidebar"] .stRadio > div { gap: 3px !important; }

[data-testid="stSidebar"] .stRadio label {
  background: transparent !important;
  border-radius: 10px !important;
  padding: 10px 14px 10px 18px !important;
  font-size: 13px !important;
  font-weight: 500 !important;
  color: var(--text-muted) !important;
  border: 1px solid transparent !important;
  transition: all 0.22s var(--ease) !important;
  cursor: pointer !important;
  width: 100% !important;
  display: block !important;
  position: relative !important;
  letter-spacing: 0.1px !important;
}

[data-testid="stSidebar"] .stRadio label:hover {
  background: rgba(124,110,250,0.09) !important;
  color: var(--text) !important;
  border-color: rgba(124,110,250,0.18) !important;
}

[data-testid="stSidebar"] .stRadio label:has(input[type="radio"]:checked) {
  background: linear-gradient(135deg, rgba(124,110,250,0.18) 0%, rgba(14,227,180,0.06) 100%) !important;
  color: #E0D9FF !important;
  border-color: rgba(124,110,250,0.38) !important;
  font-weight: 600 !important;
  box-shadow: 0 2px 16px rgba(124,110,250,0.12), inset 2px 0 0 #7C6EFA !important;
}

/* Hide radio circles */
[data-testid="stSidebar"] .stRadio > div > label > div:first-child { display: none !important; }

/* ─── BRAND BLOCK ───────────────────────────────────────── */
.brand-block {
  padding: 28px 6px 22px;
  text-align: center;
  border-bottom: 1px solid var(--border);
  margin-bottom: 18px;
}
.brand-icon-wrap {
  width: 56px; height: 56px; border-radius: 16px; margin: 0 auto 14px;
  background: linear-gradient(135deg, #7C6EFA 0%, #0EE3B4 100%);
  display: flex; align-items: center; justify-content: center;
  font-size: 26px;
  box-shadow: 0 8px 28px rgba(124,110,250,0.4), 0 0 0 1px rgba(255,255,255,0.08);
  transition: transform 0.3s var(--ease-back);
}
.brand-icon-wrap:hover { transform: rotate(-6deg) scale(1.08); }
.brand-name {
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: 17px; font-weight: 700; letter-spacing: -0.4px;
  background: linear-gradient(135deg, #C4B8FF 0%, #7C6EFA 45%, #0EE3B4 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.brand-tag {
  font-size: 10.5px; color: var(--text-muted); letter-spacing: 0.3px;
  margin-top: 4px; font-weight: 400;
}

/* ─── NAV LABEL ─────────────────────────────────────────── */
.nav-label {
  font-size: 9px; text-transform: uppercase; letter-spacing: 2px;
  color: rgba(86,99,128,0.6); font-weight: 700;
  padding: 14px 6px 5px; display: block;
}

/* ─── NAV DIVIDER ───────────────────────────────────────── */
.nav-divider {
  height: 1px; margin: 10px 4px;
  background: linear-gradient(90deg, transparent, rgba(124,110,250,0.14), transparent);
}

/* ─── USER CARD ─────────────────────────────────────────── */
.user-card {
  display: flex; align-items: center; gap: 12px;
  background: rgba(124,110,250,0.06);
  border: 1px solid var(--border); border-radius: 12px;
  padding: 12px 14px; margin: 8px 0;
}
.user-av {
  width: 36px; height: 36px; border-radius: 10px; flex-shrink: 0;
  background: linear-gradient(135deg, #7C6EFA, #0EE3B4);
  display: flex; align-items: center; justify-content: center;
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: 16px; font-weight: 700; color: #fff;
  box-shadow: 0 4px 12px rgba(124,110,250,0.3);
}
.user-name  { font-size: 13px; font-weight: 600; color: var(--text); }
.user-email { font-size: 10.5px; color: var(--text-muted); margin-top: 1px; }

/* Sign out button */
[data-testid="stSidebar"] .stButton > button {
  background: rgba(255,83,112,0.08) !important;
  color: #FF8FA3 !important;
  border: 1px solid rgba(255,83,112,0.22) !important;
  border-radius: 10px !important;
  font-size: 12.5px !important; font-weight: 600 !important;
  padding: 10px !important;
  transition: all 0.22s var(--ease) !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
  background: rgba(255,83,112,0.15) !important;
  border-color: rgba(255,83,112,0.4) !important;
  transform: translateY(-1px) !important;
}

/* ═══════════════════════════════════════════════════════════
   PAGE HEADER
═══════════════════════════════════════════════════════════ */
.page-header {
  margin-bottom: 28px;
  animation: fadeInDown 0.4s var(--ease) both;
}
.breadcrumb {
  display: inline-flex; align-items: center; gap: 7px;
  background: rgba(124,110,250,0.08); border: 1px solid rgba(124,110,250,0.18);
  border-radius: 8px; padding: 5px 14px 5px 10px; margin-bottom: 14px;
  font-size: 11.5px; color: var(--text-muted); font-weight: 500;
}
.breadcrumb-sep { color: rgba(86,99,128,0.4); }
.breadcrumb-cur { color: #A89FFF; font-weight: 600; }

.page-title {
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: 32px; font-weight: 800; letter-spacing: -1px; line-height: 1.1;
  background: linear-gradient(135deg, #EDF2F7 20%, #B8ACFF 60%, #0EE3B4 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
  margin-bottom: 7px;
}
.page-subtitle {
  font-size: 14px; color: var(--text-soft); font-weight: 400; line-height: 1.6;
  margin-bottom: 0;
}
.page-content { animation: fadeInDown 0.35s var(--ease) both; }

/* ═══════════════════════════════════════════════════════════
   KPI CARDS
═══════════════════════════════════════════════════════════ */
.kpi-card {
  background: var(--card);
  border-radius: var(--radius);
  padding: 20px 16px 18px;
  text-align: center; position: relative; overflow: hidden;
  border: 1px solid var(--border);
  transition: transform 0.28s var(--ease-back), box-shadow 0.28s var(--ease), border-color 0.22s;
  will-change: transform;
}

/* Top shimmer line */
.kpi-card::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 2px;
  background: linear-gradient(90deg, transparent 0%, #7C6EFA 35%, #0EE3B4 65%, transparent 100%);
  opacity: 0.65;
}

/* Glow blob */
.kpi-card::after {
  content: '';
  position: absolute; top: -50%; right: -30%;
  width: 130px; height: 130px;
  background: radial-gradient(circle, rgba(124,110,250,0.08) 0%, transparent 70%);
  pointer-events: none;
}

.kpi-card:hover {
  transform: translateY(-6px) scale(1.015);
  border-color: rgba(124,110,250,0.4);
  box-shadow: 0 22px 56px rgba(0,0,0,0.45), 0 0 36px rgba(124,110,250,0.1);
}

.kpi-icon {
  font-size: 24px; margin-bottom: 10px; display: block;
  filter: drop-shadow(0 0 12px rgba(124,110,250,0.5));
}
.kpi-value {
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: 28px; font-weight: 800; letter-spacing: -1px;
  background: linear-gradient(135deg, #C4B8FF 0%, #7C6EFA 50%, #0EE3B4 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
  line-height: 1;
}
.kpi-label {
  font-size: 10px; color: var(--text-muted); text-transform: uppercase;
  letter-spacing: 1.4px; margin-top: 8px; font-weight: 600;
}
.kpi-trend {
  font-size: 11px; margin-top: 7px; color: var(--secondary);
  font-weight: 500; opacity: 0.85;
}

/* ═══════════════════════════════════════════════════════════
   SECTION HEADER
═══════════════════════════════════════════════════════════ */
.section-header {
  display: flex; align-items: center; gap: 14px;
  margin: 34px 0 20px;
}
.section-header::after {
  content: ''; flex: 1; height: 1px;
  background: linear-gradient(90deg, rgba(124,110,250,0.22), transparent);
}
.section-icon {
  width: 40px; height: 40px; border-radius: 11px; flex-shrink: 0;
  background: linear-gradient(135deg, rgba(124,110,250,0.18), rgba(14,227,180,0.08));
  display: flex; align-items: center; justify-content: center;
  font-size: 18px;
  border: 1px solid rgba(124,110,250,0.28);
  box-shadow: 0 0 24px rgba(124,110,250,0.1);
}
.section-title {
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: 18px; font-weight: 700; color: var(--text); letter-spacing: -0.4px;
}
.section-subtitle { font-size: 12px; color: var(--text-muted); margin-top: 2px; font-weight: 400; }

/* ═══════════════════════════════════════════════════════════
   GLASS / CONTENT CARDS
═══════════════════════════════════════════════════════════ */
.glass-card {
  background: var(--card);
  backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
  border-radius: var(--radius); border: 1px solid var(--border);
  padding: 24px; position: relative; overflow: hidden;
  transition: border-color 0.25s var(--ease);
}
.glass-card::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(124,110,250,0.45), rgba(14,227,180,0.35), transparent);
}
.glass-card:hover { border-color: var(--border-bright); }

/* ═══════════════════════════════════════════════════════════
   INSIGHT / RECOMMENDATION CARDS
═══════════════════════════════════════════════════════════ */
.insight-card {
  background: var(--card);
  border: 1px solid var(--border); border-radius: var(--radius);
  padding: 18px 18px 18px 20px; margin-bottom: 12px;
  position: relative; overflow: hidden;
  border-left: 3px solid var(--primary) !important;
  transition: transform 0.22s var(--ease-back), box-shadow 0.22s, border-color 0.22s;
  will-change: transform;
}
.insight-card:hover {
  transform: translateX(4px);
  box-shadow: 0 8px 32px rgba(0,0,0,0.3), 0 0 20px rgba(124,110,250,0.08);
  border-color: rgba(124,110,250,0.35) !important;
}
.insight-card-title {
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: 14.5px; font-weight: 700; color: var(--text);
  margin-bottom: 7px; letter-spacing: -0.2px;
}
.insight-card-text {
  font-size: 13px; color: var(--text-soft); line-height: 1.65;
}

/* ═══════════════════════════════════════════════════════════
   WELCOME BANNER
═══════════════════════════════════════════════════════════ */
.welcome-banner {
  background: linear-gradient(135deg, rgba(124,110,250,0.1) 0%, rgba(14,227,180,0.05) 100%);
  border: 1px solid rgba(124,110,250,0.2); border-radius: var(--radius-lg);
  padding: 22px 28px; margin-bottom: 28px;
  display: flex; align-items: center; gap: 20px;
  position: relative; overflow: hidden;
  animation: fadeInDown 0.4s var(--ease) 0.1s both;
}
.welcome-banner::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
  background: linear-gradient(90deg, #7C6EFA, #0EE3B4);
}
.welcome-banner::after {
  content: ''; position: absolute;
  top: -60px; right: -60px; width: 200px; height: 200px;
  background: radial-gradient(circle, rgba(124,110,250,0.09), transparent 65%);
  pointer-events: none;
}
.welcome-avatar {
  font-size: 40px; flex-shrink: 0;
  animation: waveHand 2.2s ease-in-out 0.5s infinite;
  display: inline-block; transform-origin: 70% 70%;
}
.welcome-text-main {
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: 19px; font-weight: 700; color: var(--text); letter-spacing: -0.3px;
}
.welcome-text-sub {
  font-size: 13px; color: var(--text-soft); margin-top: 4px; line-height: 1.6;
}
.live-badge {
  display: inline-flex; align-items: center; gap: 7px;
  background: rgba(14,227,180,0.1); border: 1px solid rgba(14,227,180,0.25);
  border-radius: 6px; padding: 3px 10px;
  font-size: 11px; color: var(--secondary); font-weight: 600;
  margin-top: 9px; letter-spacing: 0.3px;
}
.live-dot {
  width: 6px; height: 6px; border-radius: 50%;
  background: var(--secondary);
  animation: blink 1.4s ease-in-out infinite;
  box-shadow: 0 0 6px var(--secondary);
}

/* ═══════════════════════════════════════════════════════════
   AI OUTPUT BOX
═══════════════════════════════════════════════════════════ */
.ai-output {
  background: linear-gradient(135deg, rgba(124,110,250,0.08) 0%, rgba(14,227,180,0.04) 100%);
  border: 1px solid rgba(124,110,250,0.24); border-radius: var(--radius);
  padding: 18px 22px; margin: 14px 0;
  position: relative; overflow: hidden;
}
.ai-output::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
  background: linear-gradient(90deg, #7C6EFA, #0EE3B4);
}
.ai-label {
  display: flex; align-items: center; gap: 8px;
  font-size: 10px; font-weight: 700; text-transform: uppercase;
  letter-spacing: 1.5px; color: var(--primary); margin-bottom: 12px;
}
.ai-dot {
  width: 7px; height: 7px; border-radius: 50%; background: var(--primary);
  animation: blink 1.6s ease-in-out infinite;
  box-shadow: 0 0 8px var(--primary);
}

/* ═══════════════════════════════════════════════════════════
   DOWNLOAD CARDS
═══════════════════════════════════════════════════════════ */
.dl-card {
  background: var(--card);
  border: 1px solid var(--border); border-radius: var(--radius);
  padding: 22px 18px 16px; margin-bottom: 12px;
  text-align: center; position: relative; overflow: hidden;
  transition: border-color 0.22s var(--ease), transform 0.22s var(--ease-back);
  will-change: transform;
}
.dl-card::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
  background: linear-gradient(90deg, #7C6EFA, #0EE3B4); opacity: 0.5;
}
.dl-card:hover { border-color: rgba(124,110,250,0.35); transform: translateY(-3px); }
.dl-icon { font-size: 32px; margin-bottom: 12px; }
.dl-title {
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: 15px; font-weight: 700; color: var(--text); margin-bottom: 6px;
}
.dl-desc { font-size: 12px; color: var(--text-muted); line-height: 1.5; margin-bottom: 14px; }

/* Download button */
.stDownloadButton > button {
  background: linear-gradient(135deg, rgba(124,110,250,0.18), rgba(14,227,180,0.1)) !important;
  color: #B8ACFF !important;
  border: 1px solid rgba(124,110,250,0.3) !important;
  border-radius: 9px !important;
  font-size: 13px !important; font-weight: 600 !important;
  transition: all 0.22s var(--ease) !important;
}
.stDownloadButton > button:hover {
  background: linear-gradient(135deg, rgba(124,110,250,0.28), rgba(14,227,180,0.15)) !important;
  border-color: rgba(124,110,250,0.5) !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 24px rgba(124,110,250,0.2) !important;
}

/* ═══════════════════════════════════════════════════════════
   STAT PILLS
═══════════════════════════════════════════════════════════ */
.stat-pill {
  display: inline-flex; align-items: center; gap: 10px;
  background: var(--card); border: 1px solid var(--border);
  border-radius: 10px; padding: 10px 16px;
  transition: border-color 0.22s;
}
.stat-pill:hover { border-color: rgba(124,110,250,0.3); }
.stat-pill-val {
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: 18px; font-weight: 700; color: var(--text);
}
.stat-pill-lbl { font-size: 11px; color: var(--text-muted); font-weight: 500; }

/* ═══════════════════════════════════════════════════════════
   CLUSTER CARDS
═══════════════════════════════════════════════════════════ */
.cluster-card {
  background: var(--card);
  border: 1px solid var(--border); border-radius: var(--radius);
  padding: 18px 18px 18px 20px;
  border-left: 3px solid var(--primary) !important;
  transition: border-color 0.22s, transform 0.22s var(--ease-back);
}
.cluster-card:hover { border-color: var(--border-bright); transform: translateX(4px); }

/* ═══════════════════════════════════════════════════════════
   METRIC BADGES
═══════════════════════════════════════════════════════════ */
.metric-badge {
  display: inline-flex; align-items: center; gap: 5px;
  padding: 3px 10px; border-radius: 6px; font-size: 11px; font-weight: 600;
}
.metric-badge-green {
  background: rgba(14,227,180,0.1); color: var(--secondary);
  border: 1px solid rgba(14,227,180,0.25);
}
.metric-badge-purple {
  background: rgba(124,110,250,0.12); color: #B8ACFF;
  border: 1px solid rgba(124,110,250,0.28);
}

/* ═══════════════════════════════════════════════════════════
   ABOUT PAGE
═══════════════════════════════════════════════════════════ */
.about-hero {
  background: linear-gradient(135deg, rgba(124,110,250,0.1) 0%, rgba(14,227,180,0.05) 100%);
  border: 1px solid rgba(124,110,250,0.22); border-radius: var(--radius-lg);
  padding: 56px 36px; text-align: center; position: relative; overflow: hidden;
}
.about-hero::before {
  content: ''; position: absolute; top: -120px; left: 50%; transform: translateX(-50%);
  width: 500px; height: 500px;
  background: radial-gradient(circle, rgba(124,110,250,0.1), transparent 65%);
  pointer-events: none;
}
.about-hero::after {
  content: ''; position: absolute; bottom: -80px; right: -80px;
  width: 250px; height: 250px;
  background: radial-gradient(circle, rgba(14,227,180,0.07), transparent 65%);
  pointer-events: none;
}

/* ═══════════════════════════════════════════════════════════
   STREAMLIT WIDGETS
═══════════════════════════════════════════════════════════ */

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
  background: rgba(7,16,30,0.9) !important;
  border-radius: 12px !important; padding: 5px !important;
  border: 1px solid var(--border) !important; gap: 3px !important;
}
.stTabs [data-baseweb="tab"] {
  color: var(--text-muted) !important; border-radius: 9px !important;
  font-weight: 500 !important; font-size: 13.5px !important;
  padding: 9px 20px !important; letter-spacing: 0.1px !important;
}
.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg, #7C6EFA, #6057D8) !important;
  color: #fff !important; font-weight: 700 !important;
  box-shadow: 0 4px 18px rgba(124,110,250,0.4) !important;
}

/* Expander */
.streamlit-expanderHeader {
  background: rgba(11,24,40,0.7) !important;
  border-radius: var(--radius-sm) !important;
  border: 1px solid var(--border) !important;
  color: var(--text-soft) !important;
  font-weight: 600 !important; font-size: 13.5px !important;
  padding: 12px 16px !important;
  transition: background 0.2s !important;
}
.streamlit-expanderHeader:hover {
  background: rgba(124,110,250,0.08) !important;
  border-color: rgba(124,110,250,0.25) !important;
}
.streamlit-expanderContent {
  background: rgba(7,16,30,0.8) !important;
  border: 1px solid var(--border) !important;
  border-top: none !important; border-radius: 0 0 var(--radius-sm) var(--radius-sm) !important;
  padding: 18px !important;
}

/* Inputs */
.stTextInput > div > div > input,
.stSelectbox > div > div > div,
.stNumberInput > div > div > input {
  background: rgba(4,9,20,0.85) !important;
  border: 1px solid rgba(124,110,250,0.22) !important;
  border-radius: 9px !important; color: var(--text) !important;
  font-size: 13.5px !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
  border-color: #7C6EFA !important;
  box-shadow: 0 0 0 3px rgba(124,110,250,0.14) !important;
}

/* Multiselect */
[data-testid="stMultiSelect"] > div {
  background: rgba(4,9,20,0.85) !important;
  border: 1px solid rgba(124,110,250,0.22) !important;
  border-radius: 9px !important;
}
[data-baseweb="tag"] {
  background: rgba(124,110,250,0.18) !important;
  border: 1px solid rgba(124,110,250,0.35) !important;
  border-radius: 6px !important;
  color: #C4B8FF !important;
}

/* Slider */
.stSlider > div > div > div > div {
  background: linear-gradient(90deg, #7C6EFA, #0EE3B4) !important;
}
[data-baseweb="slider"] [data-testid="stThumbValue"] {
  background: #7C6EFA !important; border-radius: 6px !important;
}

/* Checkbox */
.stCheckbox label { color: var(--text-soft) !important; font-size: 13px !important; }
[data-baseweb="checkbox"] [data-checked="true"] > div {
  background: #7C6EFA !important; border-color: #7C6EFA !important;
}

/* Main area buttons */
.main .stButton > button {
  background: linear-gradient(135deg, #7C6EFA, #6057D8 50%, #0EE3B4) !important;
  color: #fff !important; border: none !important;
  border-radius: 10px !important; padding: 11px 22px !important;
  font-weight: 700 !important; font-size: 14px !important;
  letter-spacing: 0.3px !important;
  transition: all 0.28s var(--ease) !important;
}
.main .stButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 10px 30px rgba(124,110,250,0.38) !important;
}

/* Labels */
label {
  color: var(--text-muted) !important; font-size: 11.5px !important;
  font-weight: 600 !important; letter-spacing: 0.4px !important;
  text-transform: uppercase !important;
}

/* Alerts */
[data-testid="stAlert"] {
  border-radius: 10px !important;
  border: 1px solid rgba(124,110,250,0.25) !important;
  background: rgba(124,110,250,0.06) !important;
}

/* DataFrame */
[data-testid="stDataFrame"] {
  border-radius: 12px !important; overflow: hidden !important;
  border: 1px solid var(--border) !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
  border: 2px dashed rgba(124,110,250,0.25) !important;
  border-radius: 12px !important; background: rgba(124,110,250,0.03) !important;
  transition: all 0.22s var(--ease) !important;
}
[data-testid="stFileUploader"]:hover {
  border-color: rgba(124,110,250,0.5) !important;
  background: rgba(124,110,250,0.07) !important;
}

/* Spinner */
.stSpinner > div > div { border-top-color: #7C6EFA !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #7C6EFA, #0EE3B4); border-radius: 4px;
}

/* HR */
hr {
  border: none !important; height: 1px !important;
  background: linear-gradient(90deg, transparent, rgba(124,110,250,0.22), transparent) !important;
  margin: 24px 0 !important;
}

/* ═══════════════════════════════════════════════════════════
   ANIMATIONS
═══════════════════════════════════════════════════════════ */
@keyframes fadeInDown {
  from { opacity: 0; transform: translateY(-12px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
  from { opacity: 0; }
  to   { opacity: 1; }
}
@keyframes blink {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0.3; }
}
@keyframes waveHand {
  0%, 60%, 100% { transform: rotate(0deg); }
  10%           { transform: rotate(18deg); }
  30%           { transform: rotate(-10deg); }
  50%           { transform: rotate(14deg); }
}
@keyframes shimmer {
  0%   { background-position: -200% 0; }
  100% { background-position:  200% 0; }
}

.page-content { animation: fadeInDown 0.35s var(--ease) both; }

/* ═══════════════════════════════════════════════════════════
   CHART WRAPPER
═══════════════════════════════════════════════════════════ */
.chart-wrap {
  background: var(--card);
  border: 1px solid var(--border); border-radius: var(--radius);
  padding: 4px 2px 2px; position: relative; overflow: hidden;
  transition: border-color 0.25s var(--ease); margin-bottom: 4px;
}
.chart-wrap::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
  background: linear-gradient(90deg, transparent, rgba(124,110,250,0.35), rgba(14,227,180,0.25), transparent);
}
.chart-wrap:hover { border-color: rgba(124,110,250,0.28); }
.chart-caption {
  font-size: 11px; color: var(--text-muted); text-align: center;
  padding: 0 12px 10px; letter-spacing: 0.3px;
}

/* ═══════════════════════════════════════════════════════════
   STAGGERED KPI ANIMATIONS
═══════════════════════════════════════════════════════════ */
[data-testid="column"]:nth-child(1) .kpi-card { animation: kpiIn 0.4s var(--ease-back) 0.05s both; }
[data-testid="column"]:nth-child(2) .kpi-card { animation: kpiIn 0.4s var(--ease-back) 0.12s both; }
[data-testid="column"]:nth-child(3) .kpi-card { animation: kpiIn 0.4s var(--ease-back) 0.19s both; }
[data-testid="column"]:nth-child(4) .kpi-card { animation: kpiIn 0.4s var(--ease-back) 0.26s both; }
@keyframes kpiIn {
  from { opacity: 0; transform: translateY(18px) scale(0.94); }
  to   { opacity: 1; transform: translateY(0) scale(1); }
}

/* ═══════════════════════════════════════════════════════════
   BETTER ALERTS
═══════════════════════════════════════════════════════════ */
[data-testid="stAlert"] {
  border-radius: 10px !important; padding: 12px 16px !important;
  border-left-width: 3px !important;
}
/* Generic fallback */
[data-testid="stAlert"] {
  background: rgba(124,110,250,0.06) !important;
  border: 1px solid rgba(124,110,250,0.22) !important;
  color: #B8ACFF !important;
}

/* ═══════════════════════════════════════════════════════════
   INFO BOX COMPONENT
═══════════════════════════════════════════════════════════ */
.info-box {
  display: flex; align-items: flex-start; gap: 10px;
  background: rgba(124,110,250,0.07); border: 1px solid rgba(124,110,250,0.2);
  border-radius: 9px; padding: 11px 14px;
  font-size: 12.5px; color: var(--text-soft); line-height: 1.6;
  margin: 8px 0;
}
.info-box-icon { color: #7C6EFA; font-size: 14px; flex-shrink: 0; margin-top: 1px; }

/* ═══════════════════════════════════════════════════════════
   MINI PROGRESS BAR
═══════════════════════════════════════════════════════════ */
.mini-progress-wrap {
  background: rgba(124,110,250,0.08); border-radius: 4px;
  height: 4px; overflow: hidden; margin-top: 10px;
}
.mini-progress-fill {
  height: 100%; border-radius: 4px;
  background: linear-gradient(90deg, #7C6EFA, #0EE3B4);
  transition: width 0.7s var(--ease);
}

/* ═══════════════════════════════════════════════════════════
   TAB PANEL PADDING
═══════════════════════════════════════════════════════════ */
.stTabs [data-baseweb="tab-panel"] { padding: 20px 0 0 !important; }

/* ═══════════════════════════════════════════════════════════
   SELECTBOX DROPDOWN THEMING
═══════════════════════════════════════════════════════════ */
[data-baseweb="popover"] [data-baseweb="menu"] {
  background: var(--bg-3) !important;
  border: 1px solid var(--border) !important; border-radius: 10px !important;
}
[data-baseweb="option"]:hover { background: rgba(124,110,250,0.1) !important; }
[data-baseweb="option"][aria-selected="true"] {
  background: rgba(124,110,250,0.15) !important; color: #B8ACFF !important;
}

/* ═══════════════════════════════════════════════════════════
   METRIC BADGE
═══════════════════════════════════════════════════════════ */
.metric-badge {
  display: inline-flex; align-items: center; gap: 5px;
  padding: 3px 10px; border-radius: 6px; font-size: 11px; font-weight: 600;
}
.metric-badge-green {
  background: rgba(14,227,180,0.1); color: var(--secondary);
  border: 1px solid rgba(14,227,180,0.25);
}
.metric-badge-purple {
  background: rgba(124,110,250,0.12); color: #B8ACFF;
  border: 1px solid rgba(124,110,250,0.28);
}
</style>
"""


def inject_css():
    st.markdown(MAIN_CSS, unsafe_allow_html=True)


def section_header(icon: str, title: str, subtitle: str = ""):
    st.markdown(
        f'<div class="section-header">'
        f'<div class="section-icon">{icon}</div>'
        f'<div>'
        f'<div class="section-title">{title}</div>'
        + (f'<div class="section-subtitle">{subtitle}</div>' if subtitle else '')
        + '</div></div>',
        unsafe_allow_html=True,
    )


def page_header(title: str, subtitle: str, breadcrumb: str = ""):
    bc = ""
    if breadcrumb:
        bc = (
            '<div class="breadcrumb">'
            '<span>🏠</span>'
            '<span class="breadcrumb-sep">›</span>'
            f'<span class="breadcrumb-cur">{breadcrumb}</span>'
            '</div>'
        )
    st.markdown(
        f'<div class="page-header page-content">'
        f'{bc}'
        f'<div class="page-title">{title}</div>'
        f'<div class="page-subtitle">{subtitle}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


# KPI icon accent colours cycle (violet, teal, amber, rose)
_KPI_COLORS = ["#7C6EFA", "#0EE3B4", "#F5C542", "#FF5370"]


def kpi_row(metrics: list):
    cols = st.columns(len(metrics))
    for idx, (col, m) in enumerate(zip(cols, metrics)):
        trend  = m.get("trend", "")
        accent = _KPI_COLORS[idx % len(_KPI_COLORS)]
        with col:
            st.markdown(
                f'<div class="kpi-card" style="--kpi-accent:{accent};">'
                f'<span class="kpi-icon" style="filter:drop-shadow(0 0 12px {accent}88);">{m["icon"]}</span>'
                f'<div class="kpi-value">{m["value"]}</div>'
                f'<div class="kpi-label">{m["label"]}</div>'
                + (f'<div class="kpi-trend" style="color:{accent};">↑ {trend}</div>' if trend else "")
                + "</div>",
                unsafe_allow_html=True,
            )


def chart_wrap(caption: str = ""):
    """Context manager wrapper — call st.plotly_chart inside it."""
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    # chart rendered by caller
    if caption:
        st.markdown(f'<div class="chart-caption">{caption}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def ai_box(text: str):
    st.markdown(
        f'<div class="ai-output">'
        f'<div class="ai-label"><div class="ai-dot"></div>AI Insight Engine</div>'
        f'{text}'
        f'</div>',
        unsafe_allow_html=True,
    )


def info_box(text: str):
    """Render a soft informational hint box."""
    st.markdown(
        f'<div class="info-box">'
        f'<span class="info-box-icon">ℹ</span>'
        f'<span>{text}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )