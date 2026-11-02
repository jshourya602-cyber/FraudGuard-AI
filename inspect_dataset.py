
import pandas as pd
from pathlib import Path


def inspect_dataset():

    file_path = (
        Path(__file__).resolve().parent
        / "dataset"
        / "transactions.csv"
    )

    data = pd.read_csv(file_path)

    print("\n================================")
    print("   FRAUDGUARD AI DATA INSPECTION")
    print("================================")

    print("\n1. Dataset Shape:")
    print(data.shape)

    print("\n2. Column Names:")
    print(data.columns.tolist())

    print("\n3. First 5 Records:")
    print(data.head())

    print("\n4. Missing Values:")
    print(data.isnull().sum())

    print("\n5. Duplicate Records:")
    print(data.duplicated().sum())

    print("\n6. Fraud Distribution:")
    print(data["is_fraud"].value_counts())

    print("\n7. Statistical Summary:")
    print(data.describe())

    print("\n================================")
    print("   INSPECTION COMPLETED")
    print("================================")


if __name__ == "__main__":
    inspect_dataset()
