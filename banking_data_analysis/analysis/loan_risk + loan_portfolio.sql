
/* Loan risk per loan (first query) */
WITH customer_risk AS (
    SELECT
        l.loan_id AS LoanID,
        c.customer_id AS CustomerID,
        c.first_name AS FirstName,
        c.last_name AS LastName,
        l.loan_amount AS LoanAmount,
        l.interest_rate AS InterestRate,
        l.term_months AS TermMonths,
        l.remaining_balance AS RemainingBalance,
        l.status AS LoanStatus
	
    FROM loans l
    JOIN customers c ON c.customer_id = l.customer_id
),
loan_risk AS (
SELECT
    *,
    CASE
        WHEN LoanStatus IN ('Paid Off', 'Active', 'Defaulted') AND (RemainingBalance / LoanAmount < 0.3 OR TermMonths IN (12, 24)) AND InterestRate < 7  THEN 'Low Risk'
        WHEN LoanStatus IN ('Delinquent','Active', 'Defaulted') AND (RemainingBalance /  LoanAmount > 0.7 OR TermMonths IN (48,60)) AND InterestRate > 12 THEN 'High Risk'
        ELSE 'Medium Risk'
	END AS LoanRisk
    FROM customer_risk
    )
    
    SELECT * FROM loan_risk;
    
    /* Loan risk in groups (second query)*/
    WITH customer_risk AS (
    SELECT
        l.loan_id AS LoanID,
        c.customer_id AS CustomerID,
        c.first_name AS FirstName,
        c.last_name AS LastName,
        l.loan_amount AS LoanAmount,
        l.interest_rate AS InterestRate,
        l.term_months AS TermMonths,
        l.remaining_balance AS RemainingBalance,
        l.status AS LoanStatus
	
    FROM loans l
    JOIN customers c ON c.customer_id = l.customer_id
),
loan_risk AS (
SELECT
    *,
    CASE
        WHEN LoanStatus IN ('Paid Off', 'Active', 'Defaulted') AND (RemainingBalance / LoanAmount < 0.3 OR TermMonths IN (12, 24)) AND InterestRate < 7  THEN 'Low Risk'
        WHEN LoanStatus IN ('Delinquent','Active', 'Defaulted') AND (RemainingBalance /  LoanAmount > 0.7 OR TermMonths IN (48,60)) AND InterestRate > 12 THEN 'High Risk'
        ELSE 'Medium Risk'
	END AS LoanRisk
    FROM customer_risk
    )
    
    SELECT 
    LoanRisk,
    COUNT(*) AS LoanCount,
    FORMAT(SUM(LoanAmount), 'N2') AS TotalLoanAmount, /*FORMAT RETURNS STRINGS*/
    FORMAT(SUM(RemainingBalance), 'N2') AS TotalRemainingBalance /*FORMAT RETURNS STRINGS*/
    FROM loan_risk
    GROUP BY 
    LoanRisk 

        