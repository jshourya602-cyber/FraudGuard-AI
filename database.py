
import mysql.connector
from mysql.connector import Error
from config import Config


def get_connection():
    """
    Establish a connection to the MySQL database.
    """

    try:
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME,
            autocommit=False
        )

        return connection

    except Error as error:
        print("MySQL Connection Error:", error)
        raise


def initialize_database():
    """
    Create the transactions table if it does not exist.
    """

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS transactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            amount DECIMAL(12,2) NOT NULL,
            transaction_hour INT NOT NULL,
            distance_from_home DECIMAL(10,2) NOT NULL,
            failed_attempts INT NOT NULL,
            account_age_days INT NOT NULL,
            prediction VARCHAR(30) NOT NULL,
            risk_score DECIMAL(6,2) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """

        cursor.execute(create_table_query)
        connection.commit()

        print("Transactions table is ready.")

    except Error as error:
        if connection:
            connection.rollback()

        print("Database Initialization Error:", error)
        raise

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


def save_transaction(
    amount,
    transaction_hour,
    distance_from_home,
    failed_attempts,
    account_age_days,
    prediction,
    risk_score
):
    """
    Save a transaction analysis result to MySQL.
    """

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
        INSERT INTO transactions (
            amount,
            transaction_hour,
            distance_from_home,
            failed_attempts,
            account_age_days,
            prediction,
            risk_score
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            amount,
            transaction_hour,
            distance_from_home,
            failed_attempts,
            account_age_days,
            prediction,
            risk_score
        )

        cursor.execute(query, values)
        connection.commit()

        return cursor.lastrowid

    except Error as error:
        if connection:
            connection.rollback()

        print("Transaction Save Error:", error)
        raise

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


def get_all_transactions():
    """
    Retrieve all stored transaction records.
    """

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT *
        FROM transactions
        ORDER BY created_at DESC, id DESC
        """

        cursor.execute(query)

        return cursor.fetchall()

    except Error as error:
        print("Transaction Retrieval Error:", error)
        raise

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


def get_filtered_transactions(
    transaction_id=None,
    prediction=None,
    risk_level=None,
    limit=10
):
    """
    Retrieve transactions using optional filters.
    """

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = "SELECT * FROM transactions"
        conditions = []
        values = []

        if transaction_id is not None:
            conditions.append("id = %s")
            values.append(transaction_id)

        if prediction in ("Fraud", "Genuine"):
            conditions.append("prediction = %s")
            values.append(prediction)

        if risk_level == "Low":
            conditions.append("risk_score <= 30")

        elif risk_level == "Medium":
            conditions.append("risk_score > 30 AND risk_score <= 70")

        elif risk_level == "High":
            conditions.append("risk_score > 70")

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY created_at DESC, id DESC LIMIT %s"
        values.append(limit)

        cursor.execute(query, tuple(values))

        return cursor.fetchall()

    except Error as error:
        print("Filtered Transaction Retrieval Error:", error)
        raise

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


def get_dashboard_statistics():
    """
    Calculate dashboard transaction statistics.
    """

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT
            COUNT(*) AS total,
            SUM(CASE WHEN prediction = 'Fraud'
                THEN 1 ELSE 0 END) AS fraud,
            SUM(CASE WHEN prediction = 'Genuine'
                THEN 1 ELSE 0 END) AS genuine,
            AVG(risk_score) AS average_risk
        FROM transactions
        """

        cursor.execute(query)

        result = cursor.fetchone()

        return {
            "total": result["total"] or 0,
            "fraud": result["fraud"] or 0,
            "genuine": result["genuine"] or 0,
            "average_risk": float(
                result["average_risk"] or 0
            )
        }

    except Error as error:
        print("Dashboard Statistics Error:", error)
        raise

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()
