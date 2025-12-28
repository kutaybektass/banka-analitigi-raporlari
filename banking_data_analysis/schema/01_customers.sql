USE banking;
DROP TABLE IF EXISTS customers;
CREATE TABLE customers (
    customer_id VARCHAR(50) PRIMARY KEY,  
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE,  
    phone VARCHAR(25),
    birth_date DATE NOT NULL,
    address TEXT,  
    city VARCHAR(100),
    state VARCHAR(50),
    zip_code VARCHAR(20),  
    country VARCHAR(100),
    join_date DATE NOT NULL,
    credit_score INT,
    customer_tier ENUM('Basic', 'Premium', 'VIP'),  
    
    CONSTRAINT chk_credit_score CHECK (credit_score BETWEEN 300 AND 850),
    CONSTRAINT chk_dates CHECK (join_date >= birth_date)  
);
