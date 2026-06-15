import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
accuracy_score,
classification_report
)

DATA_PATH = "data/credit_dataset_30000.csv"

df = pd.read_csv(DATA_PATH)

X = df.drop(
columns=[
"ID",
"default.payment.next.month"
]
)

y = df["default.payment.next.month"]

X_train, X_test, y_train, y_test = train_test_split(
X,
y,
test_size=0.20,
random_state=42,
stratify=y
)

model = LogisticRegression(
max_iter=5000
)

print("Training Logistic Regression...")

model.fit(
X_train,
y_train
)

predictions = model.predict(
X_test
)

accuracy = accuracy_score(
y_test,
predictions
)

print(
"\nAccuracy:",
round(accuracy * 100, 2),
"%"
)

print(
classification_report(
y_test,
predictions
)
)

os.makedirs(
"models",
exist_ok=True
)

joblib.dump(
model,
"models/logistic_regression.pkl"
)

print(
"\nModel saved: models/logistic_regression.pkl"
)
