SELECT
    AccountType,
	FORMAT(SUM(interest_adjusted_balance), 'N2') AS TotalProfit /* FORMAT RETURNS STRINGS */
FROM (
SELECT
    account_type AS AccountType,
    CASE
        WHEN account_type = 'Loan'
            THEN balance + balance * interest_rate
        ELSE
            balance - balance * interest_rate
    END AS interest_adjusted_balance
FROM accounts
) x
GROUP BY AccountType
ORDER BY TotalProfit DESC