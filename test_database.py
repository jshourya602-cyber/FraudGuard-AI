
from database import (
    get_connection,
    initialize_database,
    save_transaction,
    get_all_transactions,
    get_dashboard_statistics
)


def test_database():

    print("\n================================")
    print("   FRAUDGUARD AI DATABASE TEST")
    print("================================\n")

    try:

        connection = get_connection()

        print("[SUCCESS] MySQL connection established!")

        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE()")
        database_name = cursor.fetchone()[0]

        print("[SUCCESS] Connected database:", database_name)

        cursor.close()
        connection.close()

        initialize_database()

        print("[SUCCESS] Transactions table verified!")

        transaction_id = save_transaction(
            amount=1250.50,
            transaction_hour=2,
            distance_from_home=35.5,
            failed_attempts=3,
            account_age_days=12,
            prediction="Fraud",
            risk_score=92.5
        )

        print("\n[SUCCESS] Transaction inserted!")
        print("Transaction ID:", transaction_id)

        transactions = get_all_transactions()

        print("\nLatest Transaction:")
        print("------------------")

        for transaction in transactions:
            if transaction["id"] == transaction_id:
                for key, value in transaction.items():
                    print(key, ":", value)
                break

        statistics = get_dashboard_statistics()

        print("\nDashboard Statistics:")
        print("--------------------")
        print("Total Transactions:", statistics["total"])
        print("Fraud Transactions:", statistics["fraud"])
        print("Genuine Transactions:", statistics["genuine"])
        print("Average Risk:", statistics["average_risk"])

        print("\n================================")
        print("   DATABASE TEST COMPLETED")
        print("================================")

    except Exception as error:

        print("\n[FAILED] Database test failed!")
        print("Error:", error)


if __name__ == "__main__":
    test_database()
