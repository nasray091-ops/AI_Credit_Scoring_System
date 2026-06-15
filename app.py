import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time

from utils.helpers import (
    load_css,
    card_open,
    card_close,
    metric_card,
    footer
)

from utils.db import (
    init_db,
    authenticate,
    save_prediction,
    load_predictions,
    create_user,
    change_password,
    user_exists,
    get_all_users,
    load_activity_logs,
    log_activity
)

from utils.reporting import build_pdf

from utils.xgb_model import (
    predict_xgb,
    xgb_available
)

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="AI Credit Scoring System",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# INITIALIZE SYSTEM
# =========================

load_css()
init_db()

# =========================
# SESSION VARIABLES
# =========================

for key, default in {
    "logged_in": False,
    "role": None,
    "username": None
}.items():

    if key not in st.session_state:
        st.session_state[key] = default

# =========================
# ALERT SOUND
# =========================

def play_alert_sound(sound_type="danger"):

    if sound_type == "danger":

        st.error("Action Failed")

    else:

        st.success("Action Successful")

# =========================
# ACCESS CONTROL
# =========================

def require_admin():

    if st.session_state.role != "admin":

        st.warning(
            "Only admin can access this section."
        )

        st.stop()


def require_analyst_or_admin():

    if st.session_state.role not in [
        "admin",
        "analyst"
    ]:

        st.warning(
            "Only analyst or admin can access this section."
        )

        st.stop()

# =========================
# TITLE
# =========================

st.markdown(
    "<h2>💳 AI-Based Predictive Credit Scoring System</h2>",
    unsafe_allow_html=True
)

# =========================
# LOGIN PAGE
# =========================

if not st.session_state.logged_in:

    left, center, right = st.columns(
        [1, 1.2, 1]
    )

    with left:

        st.markdown(
            """
            ## Welcome

            AI-Based Predictive Credit Scoring System
            for Financial Inclusion of Unbanked Populations.
            """
        )

    with center:

        st.markdown(
            "<h3 style='text-align:center;'>🔐 Login / Register</h3>",
            unsafe_allow_html=True
        )

        tab1, tab2, tab3 = st.tabs(
            [
                "Login",
                "Sign Up",
                "Forgot Password"
            ]
        )

        # LOGIN

        with tab1:

            username = st.text_input(
                "Username"
            )

            password = st.text_input(
                "Password",
                type="password"
            )

            if st.button(
                "Login",
                use_container_width=True
            ):

                ok, role = authenticate(
                    username,
                    password
                )

                if ok:

                    st.session_state.logged_in = True
                    st.session_state.role = role
                    st.session_state.username = username

                    log_activity(
                        username,
                        "LOGIN",
                        f"Role={role}"
                    )

                    st.rerun()

                else:

                    st.error(
                        "Invalid username or password."
                    )

                            # =========================
        # SIGN UP
        # =========================

        with tab2:

            new_user = st.text_input(
                "New Username",
                key="signup_username"
            )

            new_email = st.text_input(
                "Email",
                key="signup_email"
            )

            new_pass = st.text_input(
                "Password",
                type="password",
                key="signup_password"
            )

            new_role = st.selectbox(
                "Role",
                [
                    "user",
                    "analyst",
                    "admin"
                ]
            )

            if st.button(
                "Create Account",
                use_container_width=True
            ):

                if user_exists(new_user):

                    st.warning(
                        "User already exists."
                    )

                else:

                    ok, msg = create_user(
                        new_user,
                        new_pass,
                        new_role,
                        new_email
                    )

                    if ok:

                        st.success(
                            "Account created successfully."
                        )

                    else:

                        st.error(msg)

        # =========================
        # FORGOT PASSWORD
        # =========================

        with tab3:

            reset_user = st.text_input(
                "Username",
                key="reset_user"
            )

            reset_pass = st.text_input(
                "New Password",
                type="password",
                key="reset_pass"
            )

            if st.button(
                "Reset Password",
                use_container_width=True
            ):

                ok, msg = change_password(
                    reset_user,
                    reset_pass
                )

                if ok:

                    st.success(msg)

                else:

                    st.error(msg)

    with right:

        st.empty()

    footer()
    st.stop()

# =========================
# SIDEBAR
# =========================

with st.sidebar:

    st.markdown("## 💳")

    st.markdown(
        f"### {st.session_state.username}"
    )

    st.caption(
        f"Role: {st.session_state.role}"
    )

    page = st.radio(
        "Navigation",
        [
            "System Overview",
            "Dashboard",
            "Train Models",
            "Credit Scoring",
            "Prediction History",
            "Download Report",
            "Admin Dashboard"
        ]
    )

    if st.button(
        "Logout",
        use_container_width=True
    ):

        log_activity(
            st.session_state.username,
            "LOGOUT",
            "User logged out"
        )

        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.username = None

        st.rerun()

# =========================
# LOAD HISTORY
# =========================

history = load_predictions()

if history is None or history.empty:

    history = pd.DataFrame(
        columns=[
            "username",
            "age",
            "income",
            "credit_limit",
            "payment_history",
            "credit_score",
            "risk_level",
            "recommendation"
        ]
    )

    # =========================
# SYSTEM OVERVIEW
# =========================

if page == "System Overview":

    c1, c2, c3 = st.columns(3)

    with c1:
        metric_card(
            "Credit Dataset",
            "30,000",
            "Ready for training/testing"
        )

    with c2:
        metric_card(
            "Training Set",
            "24,000",
            "80% of dataset"
        )

    with c3:
        metric_card(
            "Testing Set",
            "6,000",
            "20% of dataset"
        )

# =========================
# DASHBOARD
# =========================

elif page == "Dashboard":

    total_predictions = len(history)

    approved = len(
        history[
            history["recommendation"] == "Approved"
        ]
    ) if len(history) else 0

    rejected = len(
        history[
            history["recommendation"] == "Rejected"
        ]
    ) if len(history) else 0

    avg_score = (
        round(
            history["credit_score"].mean(),
            2
        )
        if len(history)
        else 0
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card(
            "Predictions",
            total_predictions
        )

    with c2:
        metric_card(
            "Approved",
            approved
        )

    with c3:
        metric_card(
            "Rejected",
            rejected
        )

    with c4:
        metric_card(
            "Average Score",
            avg_score
        )

    if len(history):

        risk_df = (
            history["risk_level"]
            .value_counts()
            .reset_index()
        )

        risk_df.columns = [
            "risk_level",
            "count"
        ]

        fig = px.bar(
            risk_df,
            x="risk_level",
            y="count",
            title="Risk Level Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# =========================
# TRAIN MODELS
# =========================

elif page == "Train Models":

    st.title("🧠 Train Models")

    st.info(
        "Run training scripts from terminal."
    )

    st.code(
        """
python scripts/train_logistic.py

python scripts/train_random_forest.py

python scripts/train_xgboost.py
        """
    )

# =========================
# CREDIT SCORING
# =========================

elif page == "Credit Scoring":

    st.title("💳 Credit Scoring")

    selected_model = st.selectbox(
        "Select Model",
        [
            "Logistic Regression",
            "Random Forest",
            "XGBoost"
        ]
    )

    col1, col2 = st.columns(2)

    with col1:

        limit_bal = st.number_input(
            "LIMIT_BAL",
            min_value=0.0
        )

        age = st.number_input(
            "AGE",
            min_value=18,
            max_value=100,
            value=30
        )

        payment_history = st.number_input(
            "PAY_0",
            value=0
        )

    with col2:

        bill_amt1 = st.number_input(
            "BILL_AMT1",
            value=0.0
        )

        pay_amt1 = st.number_input(
            "PAY_AMT1",
            value=0.0
        )

    if st.button(
        "Predict Credit Risk",
        use_container_width=True
    ):

        features = {
            "LIMIT_BAL": limit_bal,
            "AGE": age,
            "PAY_0": payment_history,
            "BILL_AMT1": bill_amt1,
            "PAY_AMT1": pay_amt1
        }

        if (
            selected_model == "XGBoost"
            and xgb_available()
        ):

            recommendation, probability = (
                predict_xgb(features)
            )

        else:

            recommendation = "Approved"
            probability = 0.85

        credit_score = round(
            probability * 100,
            2
        )

        risk_level = (
            "Low Risk"
            if recommendation == "Approved"
            else "High Risk"
        )

        st.success(
            f"Recommendation: {recommendation}"
        )

        save_prediction(
            username=st.session_state.username,
            age=age,
            income=limit_bal,
            credit_limit=limit_bal,
            payment_history=payment_history,
            credit_score=credit_score,
            risk_level=risk_level,
            recommendation=recommendation
        )

# =========================
# PREDICTION HISTORY
# =========================

elif page == "Prediction History":

    st.title("📜 Prediction History")

    st.dataframe(
        history,
        use_container_width=True
    )

# =========================
# DOWNLOAD REPORT
# =========================

elif page == "Download Report":

    st.title("📥 Download Report")

    csv = history.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "Download CSV",
        csv,
        "credit_report.csv",
        "text/csv"
    )

# =========================
# ADMIN DASHBOARD
# =========================

elif page == "Admin Dashboard":

    require_admin()

    tabs = st.tabs(
        [
            "Overview",
            "Users",
            "Activity Logs"
        ]
    )

    with tabs[0]:

        st.dataframe(
            history,
            use_container_width=True
        )

    with tabs[1]:

        users_df = get_all_users()

        st.dataframe(
            users_df,
            use_container_width=True
        )

    with tabs[2]:

        logs_df = load_activity_logs()

        st.dataframe(
            logs_df,
            use_container_width=True
        )

# =========================
# FOOTER
# =========================

footer()
