import streamlit as st


# ======================
# LOAD CSS
# ======================

def load_css():

    st.markdown(
        """
        <style>

        .stApp{
            background:#0F172A;
            color:white;
        }

        [data-testid="stSidebar"]{
            background:#111827;
            min-width:320px !important;
            max-width:320px !important;
        }

        /* Sidebar Navigation */

        .stRadio label{
            font-size:12px !important;
        }

        .stRadio div[role="radiogroup"] label{
            font-size:12px !important;
        }

        .stRadio p{
            font-size:12px !important;
        }

        .metric-card{
            background:#1E293B;
            padding:20px;
            border-radius:12px;
            text-align:center;
            border:1px solid #334155;
            margin-bottom:10px;
        }

        .metric-title{
            font-size:15px;
            color:#CBD5E1;
        }

        .metric-value{
            font-size:32px;
            font-weight:bold;
            color:#38BDF8;
        }

        .metric-desc{
            font-size:13px;
            color:#94A3B8;
        }

        .custom-card{
            background:#1E293B;
            padding:20px;
            border-radius:12px;
            border:1px solid #334155;
            margin-top:10px;
            margin-bottom:10px;
        }

        .stButton > button{
            width:100%;
            height:45px;
            border-radius:10px;
            font-weight:bold;
        }

        footer{
            visibility:hidden;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

# ======================
# CARD OPEN
# ======================

def card_open():

    st.markdown(
        """
        <div class="custom-card">
        """,
        unsafe_allow_html=True
    )


# ======================
# CARD CLOSE
# ======================

def card_close():

    st.markdown(
        """
        </div>
        """,
        unsafe_allow_html=True
    )


# ======================
# METRIC CARD
# ======================

def metric_card(title, value, description=""):

    st.markdown(
        f"""
### {value}

**{title}**

{description}
"""
    )

# ======================
# FOOTER
# ======================

def footer():

    st.markdown(
        """
        <hr>

        <center>

        <b>AI-Based Predictive Credit Scoring System</b>

        <br><br>

        Final Year Project

        <br><br>

        Developed using Streamlit + XGBoost

        </center>
        """,
        unsafe_allow_html=True
    )