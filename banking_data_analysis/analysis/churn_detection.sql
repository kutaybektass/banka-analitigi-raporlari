WITH customer_signals AS (
SELECT
c.customer_id,
c.first_name,
c.last_name,
MAX(CASE
    WHEN a.account_status IN ('Closed', 'Frozen') THEN 1
    ELSE 0
END) AS HasClosedAccount,
MAX(t.transaction_timestamp) AS LastTransactionDate,
SUM(a.balance) AS TotalBalance

FROM customers c
JOIN accounts a ON c.customer_id = a.customer_id
LEFT JOIN transactions t ON t.account_id = a.account_id
GROUP BY c.customer_id, c.first_name, c.last_name
)
SELECT
    *,
    CASE
        WHEN HasClosedAccount = 1 THEN 'Partially Churned'
        WHEN LastTransactionDate < CURRENT_DATE - INTERVAL 30 DAY
             AND TotalBalance < 3000 THEN 'High Risk'
        WHEN LastTransactionDate < CURRENT_DATE - INTERVAL 30 DAY
             OR TotalBalance < 3000 THEN 'Medium Risk'
        ELSE 'Low Risk'
    END AS ChurnRisk
FROM customer_signals
