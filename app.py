import streamlit as st
import pandas as pd
import requests
import os
from sklearn.linear_model import LinearRegression
import time
from streamlit_lottie import st_lottie

# LOTTIE FUNCTION

def load_lottie(url):
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except:
        return None

login_anim = load_lottie("https://assets5.lottiefiles.com/packages/lf20_tfb3estd.json")
dashboard_anim = load_lottie("https://assets2.lottiefiles.com/packages/lf20_0yfsb3a1.json")

# UI

st.set_page_config(page_title="AI Student System", layout="wide")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0E1117, #1A1D24);
    color: white;
}
.stButton>button {
    background: linear-gradient(90deg, #00C9FF, #92FE9D);
    border-radius: 10px;
    color: black;
    font-weight: bold;
}
.title {
    font-size: 40px;
    text-align: center;
    background: linear-gradient(90deg,#00C9FF,#92FE9D);
    -webkit-background-clip: text;
    color: transparent;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="title">AI Student Performance System</p>', unsafe_allow_html=True)
import os

# Firebase API KEY
API_KEY = os.getenv("FIREBASE_API_KEY")

if not API_KEY:
    raise ValueError("API Key not found! Set FIREBASE_API_KEY")

#  Firebase Auth

def login(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
    return requests.post(url, json={
        "email": email,
        "password": password,
        "returnSecureToken": True
    }).json()

def signup(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={API_KEY}"
    return requests.post(url, json={
        "email": email,
        "password": password,
        "returnSecureToken": True
    }).json()

# SESSION

if "user" not in st.session_state:
    st.session_state.user = None

menu = st.sidebar.radio("Menu", ["Login", "Signup"])

# 🔐 LOGIN

if menu == "Login" and not st.session_state.user:

    col1, col2 = st.columns([1,2])

    with col1:
        st_lottie(login_anim, height=250)

    with col2:
        st.subheader("Login")

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            res = login(email, password)

            if "idToken" in res:
                st.session_state.user = email
                st.success("Login Successful ✅")
                st.rerun()
            else:
                st.error("Invalid Credentials ❌")

#  SIGNUP

if menu == "Signup" and not st.session_state.user:

    st.subheader("Create Account")

    email = st.text_input("Email", key="s1")
    password = st.text_input("Password", type="password", key="s2")

    if st.button("Signup"):
        res = signup(email, password)

        if "idToken" in res:
            st.success("Account Created 🎉")
        else:
            st.error(res)

# DASHBOARD

if st.session_state.user:

    st.sidebar.success(f" {st.session_state.user}")

    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

    col1, col2 = st.columns([2,1])

    with col1:
        st.subheader("📊 Dashboard")

    with col2:
        st_lottie(dashboard_anim, height=150)

    # DATA SOURCE
    
    source = st.radio("Select Data Source", ["Google Sheets", "Upload CSV"])

    df = None

    if source == "Google Sheets":
        sheet_url = "https://docs.google.com/spreadsheets/d/1j_U24D5yBSvPvfZN-eC6ZXCrKa_mJKD5ysf1EumU1fY/export?format=csv"
        try:
            df = pd.read_csv(sheet_url)
            st.success("Live Data Loaded ⚡")
        except:
            st.error("Google Sheet load failed")

    if source == "Upload CSV":
        file = st.file_uploader("Upload CSV", type=["csv"])
        if file:
            df = pd.read_csv(file)
            st.success("CSV Loaded")

    # DATA DISPLAY

    if df is not None:

        st.dataframe(df)

        # 🤖 ML MODEL (UPDATED)
       
        if {"study_hours", "final_marks"}.issubset(df.columns):

            model = LinearRegression()
            model.fit(df[["study_hours"]], df["final_marks"])

            st.subheader("🤖 Predict Marks")

            hours = st.slider("Study Hours", 0, 12, 5)
            pred = model.predict([[hours]])

            st.success(f"Predicted Marks: {pred[0]:.2f}")

            # 📊 CHART
            
            st.subheader("📊 Chart")
            st.line_chart(df.set_index("study_hours")["final_marks"])

            # 🔥 PREDICT ALL + RISK
            st.subheader("🚀 Predict All Students")

            if st.button("Predict All"):

                df["Predicted Marks"] = model.predict(df[["study_hours"]])

                # Risk logic
                df["Risk Level"] = df["Predicted Marks"].apply(
                    lambda x: "High Risk 🔴" if x < 40 else "Medium 🟡" if x < 60 else "Low 🟢"
                )

                st.dataframe(df)

        else:
            st.error("CSV must contain: study_hours & final_marks")

        # 📊 POWER BI
        st.subheader("📊 Power BI Dashboard")

        powerbi_url = "https://app.powerbi.com/groups/me/reports/620da5d5-8234-4640-8fb8-76c31f599029?experience=power-bi"

        if "http" in powerbi_url:
            st.components.v1.iframe(powerbi_url, height=600)
            st.link_button("Open Dashboard", powerbi_url)
        else:
            st.warning("Add Power BI link")

        # 🔄 AUTO REFRESH
        if source == "Google Sheets":
            if st.checkbox("Auto Refresh (5 sec)"):
                time.sleep(5)
                st.rerun()

        if st.button("🔄 Refresh"):
            st.rerun()
