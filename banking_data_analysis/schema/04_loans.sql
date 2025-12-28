USE banking;
DROP TABLE IF EXISTS loans;
CREATE TABLE loans (
    loan_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    loan_amount DECIMAL(12,2) NOT NULL,
    interest_rate DECIMAL(5,3) NOT NULL,
    term_months INT NOT NULL,
    start_date DATE NOT NULL,
    monthly_payment DECIMAL(10,2) NOT NULL,
    remaining_balance DECIMAL(12,2) NOT NULL,
    collateral_description TEXT,
    status ENUM('Active', 'Delinquent', 'Paid Off', 'Defaulted') DEFAULT 'Active',
    
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    
    CONSTRAINT chk_loans_loan_amount CHECK (loan_amount > 0),
    CONSTRAINT chk_loans_interest_rate CHECK (interest_rate BETWEEN 1.000 AND 25.000), 
    CONSTRAINT chk_loans_term CHECK (term_months BETWEEN 12 AND 360),
    CONSTRAINT chk_loans_remaining_balance CHECK (remaining_balance >= 0 AND remaining_balance <= loan_amount),
    CONSTRAINT chk_loans_monthly_payment CHECK (monthly_payment > 0),
    CONSTRAINT chk_loans_start_date CHECK (start_date >= '2000-01-01')
);
