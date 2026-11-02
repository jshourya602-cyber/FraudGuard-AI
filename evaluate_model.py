
import pandas as pd
import joblib
from pathlib import Path
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    accuracy_score
)


def evaluate_model():

    base_folder = Path(__file__).resolve().parent

    model_path = base_folder / "model" / "fraud_model.pkl"

    dataset_path = (
        base_folder / "dataset" / "transactions.csv"
    )

    model = joblib.load(model_path)

    data = pd.read_csv(dataset_path)

    X = data.drop("is_fraud", axis=1)
    y_actual = data["is_fraud"]

    predictions = model.predict(X)

    y_predicted = pd.Series(predictions).map({
        1: 0,
        -1: 1
    })

    accuracy = accuracy_score(y_actual, y_predicted)

    matrix = confusion_matrix(y_actual, y_predicted)

    print("\n================================")
    print("   FRAUDGUARD AI MODEL EVALUATION")
    print("================================")

    print("\nAccuracy:", round(accuracy * 100, 2), "%")

    print("\nConfusion Matrix:")
    print(matrix)

    print("\nClassification Report:")
    print(
        classification_report(
            y_actual,
            y_predicted,
            target_names=["Genuine", "Fraud"]
        )
    )

    print("\n================================")
    print("   EVALUATION COMPLETED")
    print("================================")


if __name__ == "__main__":
    evaluate_model()
