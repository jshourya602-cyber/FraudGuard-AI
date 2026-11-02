
from flask import Flask, render_template, request, jsonify, abort
from transaction_analyzer import analyze_transaction
from database import (
    get_all_transactions,
    get_filtered_transactions,
    get_dashboard_statistics
)

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        amount = float(request.form["amount"])
        transaction_hour = int(request.form["transaction_hour"])
        distance_from_home = float(request.form["distance_from_home"])
        failed_attempts = int(request.form["failed_attempts"])
        account_age_days = int(request.form["account_age_days"])

        if (
            amount <= 0
            or not 0 <= transaction_hour <= 23
            or distance_from_home < 0
            or failed_attempts < 0
            or account_age_days < 1
        ):
            return jsonify({
                "error": "Please enter valid transaction details."
            }), 400

        result = analyze_transaction(
            amount,
            transaction_hour,
            distance_from_home,
            failed_attempts,
            account_age_days
        )

        return jsonify(result)

    except (ValueError, KeyError):
        return jsonify({
            "error": "Invalid transaction input."
        }), 400

    except Exception:
        app.logger.exception("Transaction analysis failed")
        return jsonify({
            "error": "Transaction analysis failed. Please try again."
        }), 500


@app.route("/dashboard")
def dashboard():
    statistics = get_dashboard_statistics()

    transaction_id = request.args.get("transaction_id", "").strip()
    prediction = request.args.get("prediction", "").strip()
    risk_level = request.args.get("risk_level", "").strip()

    if transaction_id and not transaction_id.isdigit():
        transaction_id = ""

    if prediction not in ("Fraud", "Genuine"):
        prediction = None

    if risk_level not in ("Low", "Medium", "High"):
        risk_level = None

    if transaction_id:
        transaction_id = int(transaction_id)
    else:
        transaction_id = None

    transactions = get_filtered_transactions(
        transaction_id=transaction_id,
        prediction=prediction,
        risk_level=risk_level,
        limit=10
    )

    return render_template(
        "dashboard.html",
        statistics=statistics,
        transactions=transactions,
        selected_transaction_id=transaction_id or "",
        selected_prediction=prediction or "",
        selected_risk_level=risk_level or ""
    )


@app.route("/transaction/<int:transaction_id>")
def transaction_details(transaction_id):

    transactions = get_all_transactions()

    transaction = next(
        (
            item for item in transactions
            if item["id"] == transaction_id
        ),
        None
    )

    if transaction is None:
        abort(404)

    risk_score = float(transaction["risk_score"])

    if risk_score <= 30:
        risk_level = "Low"
    elif risk_score <= 70:
        risk_level = "Medium"
    else:
        risk_level = "High"

    return render_template(
        "transaction_details.html",
        transaction=transaction,
        risk_level=risk_level
    )


if __name__ == "__main__":
    app.run(debug=True)
