import os
import joblib
import pandas as pd

MODEL_PATH = "models/xgboost_model.pkl"


# ======================
# CHECK MODEL
# ======================

def xgb_available():

    return os.path.exists(
        MODEL_PATH
    )


# ======================
# LOAD MODEL
# ======================

def load_model():

    if not xgb_available():

        raise FileNotFoundError(
            f"Model not found: {MODEL_PATH}"
        )

    return joblib.load(
        MODEL_PATH
    )


# ======================
# PREDICT
# ======================

def predict_xgb(features):

    model = load_model()

    df = pd.DataFrame(
        [features]
    )

    prediction = model.predict(
        df
    )[0]

    probability = float(
        model.predict_proba(df)[0][1]
    )

    recommendation = (
        "Approved"
        if prediction == 1
        else "Rejected"
    )

    return (
        recommendation,
        probability
    )