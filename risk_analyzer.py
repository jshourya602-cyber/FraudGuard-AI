
import pandas as pd
import joblib
from pathlib import Path


def analyze_risk():

    base_folder = Path(__file__).resolve().parent

    model_path = base_folder / "model" / "fraud_model.pkl"

    dataset_path = (
        base_folder / "dataset" / "transactions.csv"
    )

    model = joblib.load(model_path)

    data = pd.read_csv(dataset_path)

    X = data.drop("is_fraud", axis=1)

    predictions = model.predict(X)

    anomaly_scores = model.decision_function(X)

    risk_scores = (
        (anomaly_scores.max() - anomaly_scores)
        /
        (anomaly_scores.max() - anomaly_scores.min())
    ) * 100

    data["prediction"] = pd.Series(predictions).map({
        1: "Genuine",
        -1: "Fraud"
    })

    data["risk_score"] = risk_scores.round(2)

    data["risk_level"] = pd.cut(
        data["risk_score"],
        bins=[-1, 30, 70, 100],
        labels=["Low", "Medium", "High"]
    )

    print("\n================================")
    print("   FRAUDGUARD AI RISK ANALYSIS")
    print("================================")

    print("\nFirst 10 Transaction Risk Scores:")

    print(
        data[
            ["amount", "prediction", "risk_score", "risk_level"]
        ].head(10)
    )

    print("\nRisk Level Distribution:")

    print(data["risk_level"].value_counts())

    print("\n================================")
    print("   RISK ANALYSIS COMPLETED")
    print("================================")


if __name__ == "__main__":
    analyze_risk()
