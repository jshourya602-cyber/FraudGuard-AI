
const form = document.getElementById("transactionForm");
const resultDiv = document.getElementById("result");

form.addEventListener("submit", async function (event) {
    event.preventDefault();

    resultDiv.innerHTML = "Analyzing transaction...";

    try {
        const response = await fetch("/analyze", {
            method: "POST",
            body: new FormData(form)
        });

        const result = await response.json();

        if (!response.ok) {
            resultDiv.innerHTML = result.error;
            return;
        }

        resultDiv.innerHTML = `
            <h2>Analysis Result</h2>
            <p><strong>Transaction ID:</strong> ${result.transaction_id}</p>
            <p><strong>Prediction:</strong> ${result.prediction}</p>
            <p><strong>Risk Score:</strong> ${result.risk_score}%</p>
            <p><strong>Risk Level:</strong> ${result.risk_level}</p>
        `;

    } catch (error) {
        resultDiv.innerHTML = "Unable to connect to the server.";
    }
});
