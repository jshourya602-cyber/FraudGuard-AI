
import pandas as pd
from pathlib import Path
from sklearn.ensemble import IsolationForest
import joblib


def train_model():

    file_path = (
        Path(__file__).resolve().parent
        / "dataset"
        / "transactions.csv"
    )

    data = pd.read_csv(file_path)

    X = data.drop("is_fraud", axis=1)

    model = IsolationForest(
        n_estimators=100,
        contamination=0.05,
        random_state=42
    )

    model.fit(X)

    model_folder = Path(__file__).resolve().parent / "model"
    model_folder.mkdir(exist_ok=True)

    model_path = model_folder / "fraud_model.pkl"

    joblib.dump(model, model_path)

    print("\n================================")
    print("   FRAUDGUARD AI MODEL TRAINING")
    print("================================")

    print("\nAlgorithm: Isolation Forest")
    print("Training Records:", len(X))
    print("Input Features:", len(X.columns))
    print("Contamination: 0.05")

    print("\nModel trained successfully!")
    print("Model saved at:", model_path)

    print("\n================================")


if __name__ == "__main__":
    train_model()
