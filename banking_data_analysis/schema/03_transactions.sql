USE BANKING;
DROP TABLE IF EXISTS transactions;
CREATE TABLE transactions (
    transaction_id VARCHAR(50) PRIMARY KEY,
    account_id VARCHAR(50) NOT NULL,
    transaction_type ENUM('Deposit', 'Withdrawal', 'Transfer', 'Payment', 'Fee'),
    amount DECIMAL(12,2) NOT NULL,  
    transaction_timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    description TEXT,
    merchant_name VARCHAR(255) NULL,
    merchant_category VARCHAR(100) NULL,
    status ENUM('Pending', 'Completed', 'Failed', 'Cancelled') DEFAULT 'Pending',
    balance_after DECIMAL(15,2),  
    
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    
    CONSTRAINT chk_amount_not_zero CHECK (amount != 0)
);