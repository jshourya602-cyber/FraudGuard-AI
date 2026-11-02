
import pandas as pd
import joblib
from pathlib import Path


def test_model():

    base_folder = Path(__file__).resolve().parent

    model_path = base_folder / "model" / "fraud_model.pkl"

    dataset_path = (
        base_folder / "dataset" / "transactions.csv"
    )

    model = joblib.load(model_path)

    data = pd.read_csv(dataset_path)

    X = data.drop("is_fraud", axis=1)

    predictions = model.predict(X)

    data["prediction"] = predictions

    data["prediction"] = data["prediction"].map({
        1: "Genuine",
        -1: "Fraud"
    })

    print("\n================================")
    print("   FRAUDGUARD AI MODEL TEST")
    print("================================")

    print("\nFirst 10 Predictions:")
    print(data[["is_fraud", "prediction"]].head(10))

    print("\nPrediction Distribution:")
    print(data["prediction"].value_counts())

    print("\n================================")
    print("   MODEL TEST COMPLETED")
    print("================================")


if __name__ == "__main__":
    test_model()
