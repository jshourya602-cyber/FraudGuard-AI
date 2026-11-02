
import pandas as pd
from pathlib import Path


def prepare_data():

    file_path = (
        Path(__file__).resolve().parent
        / "dataset"
        / "transactions.csv"
    )

    data = pd.read_csv(file_path)

    X = data.drop("is_fraud", axis=1)

    y = data["is_fraud"]

    print("\n================================")
    print("   FRAUDGUARD AI DATA PREPARATION")
    print("================================")

    print("\nInput Features:")
    print(X.columns.tolist())

    print("\nInput Data Shape:")
    print(X.shape)

    print("\nActual Labels Shape:")
    print(y.shape)

    print("\nData Preparation Completed!")

    print("\n================================")


if __name__ == "__main__":
    prepare_data()
