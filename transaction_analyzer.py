
import pandas as pd
import joblib
from pathlib import Path
from database import save_transaction


def analyze_transaction(
    amount,
    transaction_hour,
    distance_from_home,
    failed_attempts,
    account_age_days
):

    base_folder = Path(__file__).resolve().parent

    model_path = base_folder / "model" / "fraud_model.pkl"

    model = joblib.load(model_path)

    transaction = pd.DataFrame([{
        "amount": amount,
        "transaction_hour": transaction_hour,
        "distance_from_home": distance_from_home,
        "failed_attempts": failed_attempts,
        "account_age_days": account_age_days
    }])

    prediction = model.predict(transaction)[0]

    anomaly_score = model.decision_function(transaction)[0]

    training_data_path = (
        base_folder / "dataset" / "transactions.csv"
    )

    training_data = pd.read_csv(training_data_path)

    training_scores = model.decision_function(
        training_data.drop("is_fraud", axis=1)
    )

    risk_score = (
        (training_scores.max() - anomaly_score)
        /
        (training_scores.max() - training_scores.min())
    ) * 100

    risk_score = round(
        max(0, min(100, risk_score)),
        2
    )

    prediction_result = (
        "Fraud" if prediction == -1 else "Genuine"
    )

    risk_level = (
        "Low" if risk_score <= 30
        else "Medium" if risk_score <= 70
        else "High"
    )

    transaction_id = save_transaction(
        amount=amount,
        transaction_hour=transaction_hour,
        distance_from_home=distance_from_home,
        failed_attempts=failed_attempts,
        account_age_days=account_age_days,
        prediction=prediction_result,
        risk_score=risk_score
    )

    return {
        "transaction_id": transaction_id,
        "prediction": prediction_result,
        "risk_score": risk_score,
        "risk_level": risk_level
    }


if __name__ == "__main__":

    result = analyze_transaction(
        amount=50000,
        transaction_hour=2,
        distance_from_home=150,
        failed_attempts=4,
        account_age_days=10
    )

    print("\n================================")
    print("   FRAUDGUARD AI TRANSACTION")
    print("================================")

    print("Transaction ID:", result["transaction_id"])
    print("Prediction:", result["prediction"])
    print("Risk Score:", result["risk_score"])
    print("Risk Level:", result["risk_level"])

    print("\nTransaction saved in MySQL!")

    print("\n================================")
