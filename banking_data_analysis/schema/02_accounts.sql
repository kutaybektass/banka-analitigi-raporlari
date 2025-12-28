USE banking;
DROP TABLE IF EXISTS accounts;
CREATE TABLE accounts (
    account_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    balance DECIMAL(15,2) NOT NULL DEFAULT 0.00,  
    opening_date DATE NOT NULL,
    account_type ENUM('Checking', 'Savings', 'Money Market', 'CD', 'Loan'),
    account_status ENUM('Open', 'Closed', 'Frozen') DEFAULT 'Open',
    overdraft_limit DECIMAL(10,2) DEFAULT 0.00,
    last_transaction_date DATE,  
    interest_rate DECIMAL(5,3),   
    
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    
    CONSTRAINT chk_positive_balance CHECK (balance >= 0),
    CONSTRAINT chk_overdraft_limit CHECK (overdraft_limit BETWEEN 0 AND 10000),
    CONSTRAINT chk_interest_rate CHECK (interest_rate BETWEEN 0 AND 25.000)

);
