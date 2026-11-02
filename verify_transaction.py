
from database import get_all_transactions


def verify_transaction():

    transactions = get_all_transactions()

    print("\n================================")
    print("   FRAUDGUARD AI DATABASE CHECK")
    print("================================")

    print("\nTotal Saved Transactions:", len(transactions))

    print("\nLatest Transaction:")

    if transactions:

        transaction = transactions[0]

        for key, value in transaction.items():
            print(f"{key}: {value}")

    else:

        print("No transactions found.")

    print("\n================================")


if __name__ == "__main__":
    verify_transaction()
