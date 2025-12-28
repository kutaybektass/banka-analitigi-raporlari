WITH suspicious_amounts AS (
SELECT 
c.customer_id AS CustomerId, 
c.first_name AS FirstName, 
c.last_name AS LastName, 
a.account_id AS AccountId, 
t.transaction_id AS TransactionID, 
t.amount AS TransferedAmount,
t.transaction_timestamp AS TransactionDate
FROM transactions t
JOIN accounts a ON t.account_id = a.account_id
JOIN customers c ON a.customer_id = c.customer_id
WHERE a.account_type IN ('Savings', 'Checking', 'Loan') AND t.amount BETWEEN 9000 AND 9999
),
suspicious_counts AS (
SELECT 
*,
COUNT(*) OVER(
PARTITION BY CustomerId
ORDER BY TransactionDate
RANGE BETWEEN INTERVAL 30 DAY PRECEDING AND CURRENT ROW
) AS 30DayCount
FROM suspicious_amounts
)
SELECT * FROM suspicious_counts
WHERE 30DayCount >= 3
