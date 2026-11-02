
import pandas as pd
import numpy as np
from pathlib import Path


def generate_dataset():

    np.random.seed(42)

    total_transactions = 5000
    fraud_count = 250
    genuine_count = total_transactions - fraud_count

    genuine = pd.DataFrame({
        "amount": np.random.lognormal(6, 1, genuine_count),
        "transaction_hour": np.random.randint(6, 23, genuine_count),
        "distance_from_home": np.random.exponential(5, genuine_count),
        "failed_attempts": np.random.choice(
            [0, 1, 2], genuine_count, p=[0.85, 0.12, 0.03]
        ),
        "account_age_days": np.random.randint(
            100, 3000, genuine_count
        ),
        "is_fraud": 0
    })

    fraud = pd.DataFrame({
        "amount": np.random.lognormal(8, 1, fraud_count),
        "transaction_hour": np.random.choice(
            [0, 1, 2, 3, 4, 23],
            fraud_count
        ),
        "distance_from_home": np.random.uniform(
            30, 500, fraud_count
        ),
        "failed_attempts": np.random.choice(
            [2, 3, 4, 5],
            fraud_count,
            p=[0.15, 0.35, 0.30, 0.20]
        ),
        "account_age_days": np.random.randint(
            1, 180, fraud_count
        ),
        "is_fraud": 1
    })

    dataset = pd.concat(
        [genuine, fraud],
        ignore_index=True
    )

    dataset = dataset.sample(
        frac=1,
        random_state=42
    ).reset_index(drop=True)

    dataset["amount"] = dataset["amount"].round(2)
    dataset["distance_from_home"] = (
        dataset["distance_from_home"].round(2)
    )

    dataset_folder = Path(__file__).resolve().parent / "dataset"
    dataset_folder.mkdir(exist_ok=True)

    file_path = dataset_folder / "transactions.csv"

    dataset.to_csv(file_path, index=False)

    print("\n================================")
    print("   FRAUDGUARD AI DATASET")
    print("================================")

    print("\nDataset generated successfully!")

    print("Total Transactions:", len(dataset))
    print("Genuine Transactions:", (dataset["is_fraud"] == 0).sum())
    print("Fraud Transactions:", (dataset["is_fraud"] == 1).sum())

    print("\nDataset Location:", file_path)

    print("\nFirst 5 Records:")
    print(dataset.head())

    print("\n================================")


if __name__ == "__main__":
    generate_dataset()
