"""
Premium Auth UI — Black Friday Intelligence Dashboard
Glassmorphism login & signup with animated accents
"""

import streamlit as st
import hashlib, json, os, base64
from datetime import datetime

# Always resolve paths relative to this file, not the cwd
_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(_DIR, "users.json")
_LOGO_PATH = os.path.join(_DIR, "logo.png")

def _get_logo_b64() -> str:
    if not os.path.exists(_LOGO_PATH):
        return ""
    with open(_LOGO_PATH, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()

_LOGO_B64 = _get_logo_b64()

def hash_password(p): return hashlib.sha256(p.encode()).hexdigest()

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE) as f:
            return json.load(f)
    default = {"demo@blackfriday.ai": {"name": "Demo Analyst", "password": hash_password("demo123"), "created": str(datetime.now())}}
    save_users(default); return default

def save_users(u):
    with open(USERS_FILE, "w") as f: json.dump(u, f, indent=2)

def login_user(email, password):
    users = load_users()
    if email in users and users[email]["password"] == hash_password(password):
        st.session_state.update(authenticated=True, user_email=email, user_name=users[email]["name"])
        return True
    return False

def signup_user(name, email, password):
    users = load_users()
    if email in users: return False, "Email already registered."
    if len(password) < 6: return False, "Password must be at least 6 characters."
    users[email] = {"name": name, "password": hash_password(password), "created": str(datetime.now())}
    save_users(users); return True, "Account created!"

def logout():
    for k in ["authenticated", "user_email", "user_name"]:
        st.session_state.pop(k, None)

def is_authenticated(): return st.session_state.get("authenticated", False)


def render_auth_page():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600;12..96,700;12..96,800&family=DM+Sans:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
      font-family: 'DM Sans', sans-serif !important;
      -webkit-font-smoothing: antialiased !important;
    }

    .stApp {
      background: #040A14 !important;
      background-image:
        radial-gradient(ellipse 80% 60% at 10% 5%,  rgba(124,110,250,0.14) 0%, transparent 55%),
        radial-gradient(ellipse 60% 50% at 90% 95%, rgba(14,227,180,0.09) 0%, transparent 50%) !important;
    }

    /* Animated dot grid */
    .stApp::before {
      content: '';
      position: fixed; inset: 0;
      background-image: radial-gradient(circle, rgba(124,110,250,0.07) 1px, transparent 1px);
      background-size: 28px 28px;
      pointer-events: none; z-index: 0;
      animation: gridPulse 8s ease-in-out infinite alternate;
    }
    @keyframes gridPulse {
      from { opacity: 0.6; }
      to   { opacity: 1;   }
    }

    #MainMenu, footer, header { visibility: hidden !important; }
    .block-container { padding: 0 !important; }

    /* ── Auth layout ── */
    .auth-outer {
      min-height: 100vh;
      display: flex; align-items: center; justify-content: center;
      padding: 40px 16px;
    }

    /* ── Auth card ── */
    .auth-card {
      width: 100%; max-width: 420px;
      background: linear-gradient(160deg, rgba(11,24,40,0.94), rgba(7,16,30,0.97));
      backdrop-filter: blur(28px); -webkit-backdrop-filter: blur(28px);
      border-radius: 22px;
      border: 1px solid rgba(124,110,250,0.2);
      box-shadow:
        0 48px 96px rgba(0,0,0,0.6),
        0 0 0 1px rgba(255,255,255,0.03),
        inset 0 1px 0 rgba(255,255,255,0.06);
      padding: 44px 38px 36px;
      position: relative; overflow: hidden;
      animation: slideUp 0.55s cubic-bezier(0.22,1,0.36,1) both;
    }
    @keyframes slideUp {
      from { opacity: 0; transform: translateY(28px) scale(0.97); }
      to   { opacity: 1; transform: translateY(0) scale(1); }
    }

    /* Top accent line */
    .auth-card::before {
      content: ''; position: absolute;
      top: 0; left: 20%; right: 20%; height: 2px;
      background: linear-gradient(90deg, transparent, #7C6EFA 35%, #0EE3B4 65%, transparent);
      border-radius: 0 0 2px 2px;
    }

    /* Corner glow */
    .auth-card::after {
      content: '';
      position: absolute; top: -100px; right: -100px;
      width: 280px; height: 280px;
      background: radial-gradient(circle, rgba(124,110,250,0.08), transparent 65%);
      pointer-events: none;
    }

    .auth-icon {
      width: 60px; height: 60px; border-radius: 16px; margin: 0 auto 18px;
      background: linear-gradient(135deg, #7C6EFA 0%, #0EE3B4 100%);
      display: flex; align-items: center; justify-content: center;
      font-size: 26px;
      box-shadow: 0 10px 32px rgba(124,110,250,0.42), 0 0 0 1px rgba(255,255,255,0.07);
      animation: iconFloat 4s ease-in-out infinite alternate;
    }
    @keyframes iconFloat {
      from { transform: translateY(0); box-shadow: 0 10px 32px rgba(124,110,250,0.42); }
      to   { transform: translateY(-5px); box-shadow: 0 18px 42px rgba(124,110,250,0.55); }
    }

    .auth-title {
      font-family: 'Bricolage Grotesque', sans-serif;
      font-size: 24px; font-weight: 800; text-align: center;
      background: linear-gradient(135deg, #C4B8FF 0%, #7C6EFA 45%, #0EE3B4 100%);
      -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
      letter-spacing: -0.6px; margin-bottom: 5px;
    }
    .auth-subtitle {
      text-align: center; font-size: 13px; color: rgba(160,171,190,0.75);
      margin-bottom: 28px; line-height: 1.55;
    }

    .demo-box {
      background: rgba(124,110,250,0.07);
      border: 1px solid rgba(124,110,250,0.2); border-radius: 11px;
      padding: 13px 16px; text-align: center;
      color: rgba(160,171,190,0.85); font-size: 12.5px;
      margin-top: 20px; line-height: 1.75;
    }
    .demo-box strong { color: #0EE3B4; font-weight: 600; }

    /* Inputs */
    .stTextInput > div > div > input {
      background: rgba(4,9,20,0.9) !important;
      border: 1px solid rgba(124,110,250,0.22) !important;
      border-radius: 10px !important; color: #EDF2F7 !important;
      font-size: 14px !important; padding: 12px 14px !important;
      font-family: 'DM Sans', sans-serif !important;
      transition: all 0.25s ease !important;
    }
    .stTextInput > div > div > input:focus {
      border-color: #7C6EFA !important;
      box-shadow: 0 0 0 3px rgba(124,110,250,0.14) !important;
      outline: none !important;
    }
    .stTextInput > div > div > input::placeholder { color: rgba(86,99,128,0.6) !important; }

    /* Buttons */
    .stButton > button {
      background: linear-gradient(135deg, #7C6EFA 0%, #6057D8 50%, #0EE3B4 100%) !important;
      color: #fff !important; border: none !important;
      border-radius: 11px !important; padding: 13px 24px !important;
      font-weight: 700 !important; font-size: 14.5px !important;
      font-family: 'DM Sans', sans-serif !important;
      width: 100% !important; letter-spacing: 0.2px !important;
      transition: all 0.3s cubic-bezier(0.22,1,0.36,1) !important;
      margin-top: 6px !important;
      box-shadow: 0 4px 20px rgba(124,110,250,0.25) !important;
    }
    .stButton > button:hover {
      transform: translateY(-2px) !important;
      box-shadow: 0 12px 36px rgba(124,110,250,0.45) !important;
    }
    .stButton > button:active { transform: translateY(0) !important; }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
      background: rgba(4,9,20,0.8) !important;
      border-radius: 12px !important; padding: 5px !important;
      border: 1px solid rgba(124,110,250,0.15) !important; gap: 3px !important;
    }
    .stTabs [data-baseweb="tab"] {
      color: rgba(160,171,190,0.8) !important;
      border-radius: 9px !important; font-weight: 600 !important;
      font-size: 13.5px !important; padding: 9px 22px !important;
    }
    .stTabs [aria-selected="true"] {
      background: linear-gradient(135deg, #7C6EFA, #6057D8) !important;
      color: #fff !important; box-shadow: 0 4px 18px rgba(124,110,250,0.4) !important;
    }

    .stCheckbox label {
      color: rgba(160,171,190,0.8) !important;
      font-size: 13px !important; font-weight: 500 !important;
      text-transform: none !important; letter-spacing: 0 !important;
    }
    label {
      color: rgba(86,99,128,0.9) !important; font-size: 11.5px !important;
      font-weight: 600 !important; letter-spacing: 0.4px !important;
      text-transform: uppercase !important;
    }
    </style>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        # Build logo HTML — image if available, emoji fallback
        _logo_tag = (
            f'<img src="{_LOGO_B64}" style="width:60px;height:60px;border-radius:16px;'
            'box-shadow:0 10px 32px rgba(124,110,250,0.42);display:block;margin:0 auto 16px;">'
            if _LOGO_B64
            else '<div style="width:60px;height:60px;border-radius:16px;margin:0 auto 16px;'
                 'background:linear-gradient(135deg,#7C6EFA,#0EE3B4);'
                 'display:flex;align-items:center;justify-content:center;font-size:26px;'
                 'box-shadow:0 10px 32px rgba(124,110,250,0.42);">\U0001f6cd\ufe0f</div>'
        )
        st.markdown(f"""
        <div style="padding-top:36px;">
          <div style="text-align:center;margin-bottom:4px;">
            {_logo_tag}
            <div style="font-family:'Bricolage Grotesque',sans-serif;font-size:24px;font-weight:800;
                        background:linear-gradient(135deg,#C4B8FF,#7C6EFA,#0EE3B4);
                        -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                        letter-spacing:-0.6px;">Black Friday AI</div>
            <div style="font-size:13px;color:rgba(160,171,190,0.7);margin-top:5px;margin-bottom:26px;">
              Intelligence Dashboard · Data Mining Suite
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["🔑  Sign In", "✨  Create Account"])

        with tab1:
            with st.form("login_form"):
                email    = st.text_input("Email Address", placeholder="demo@blackfriday.ai")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                st.checkbox("Keep me signed in", value=True)
                submitted = st.form_submit_button("Sign In  →")

            if submitted:
                if not email or not password:
                    st.error("Please fill in all fields.")
                elif login_user(email, password):
                    st.success("Welcome back! Loading dashboard…")
                    st.rerun()
                else:
                    st.error("Invalid email or password.")

            st.markdown("""
            <div class="demo-box">
              🎯 &nbsp;Demo credentials<br>
              Email: <strong>demo@blackfriday.ai</strong> &nbsp;·&nbsp; Password: <strong>demo123</strong>
            </div>
            """, unsafe_allow_html=True)

        with tab2:
            with st.form("signup_form"):
                name     = st.text_input("Full Name", placeholder="Jane Doe")
                email_s  = st.text_input("Email Address", placeholder="you@example.com", key="se")
                pass_s   = st.text_input("Password", type="password", placeholder="Min 6 characters", key="sp")
                sub_s    = st.form_submit_button("Create Account  →")

            if sub_s:
                if not name or not email_s or not pass_s:
                    st.error("Please fill in all fields.")
                else:
                    ok, msg = signup_user(name, email_s, pass_s)
                    (st.success if ok else st.error)(msg + (" Please log in." if ok else ""))