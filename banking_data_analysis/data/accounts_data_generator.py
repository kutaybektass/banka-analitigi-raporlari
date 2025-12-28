import random
from faker import Faker
import mysql.connector
from datetime import date, timedelta
from uuid import uuid4

conn = mysql.connector.connect(host = 'localhost', user = 'root', password = '', database = 'banking')
cursor = conn.cursor()
cursor.execute('SELECT customer_id, birth_date FROM customers')

customer_ids = []
customer_birth_dates = []
for i, j in cursor.fetchall():
    customer_ids.append(i)
    customer_birth_dates.append(j)

cursor.close()
conn.close()

fake = Faker()
fake.unique.clear()


def balance_check(type, status):
    if status == 'Closed':
        return 0.00
    
    if type == 'Checking':
        return random.triangular(500.00, 5000.00, 1500.00)
    elif type == 'Savings':
        return random.triangular(1000.00, 50000.00, 5000)
    elif type == 'Money Market':
        return random.triangular(10000.00, 200000.00, 25000.00)
    else:
        return random.choice([5000.00, 1000.00, 25000.00, 50000.00, 100000.00])

def overdraft_check(type):
    if type == 'Checking':
        return random.uniform(100.00, 5000.00)
    else:
        return 0
    
def interest_check(type, status):
    if status == 'Closed':
        return 0
    
    if type == 'Checking':
        return random.uniform(0.01, 0.1)
    elif type == 'Savings':
        return random.uniform(0.5, 2.5)
    elif type == 'Money Market':
        return random.uniform(1.5, 3)
    else: #CD
        return random.uniform(2, 5)
    
def date_check(status, customer_birth_date):
    today = date.today()
    min_opening = customer_birth_date + timedelta(days=18*365)
    
    if status == 'Closed':
        
        max_opening = today - timedelta(days=30)
        
        if min_opening >= max_opening:
            min_opening = max_opening - timedelta(days=365*5)  
        
        opening_date = fake.date_between(start_date=min_opening, end_date=max_opening)
        
        days_opened = (today - opening_date).days
        if days_opened > 1:
            last_transaction = fake.date_between(
                start_date=opening_date,
                end_date=opening_date + timedelta(days=random.randint(1, days_opened))
            )
        else:
            last_transaction = opening_date  
        
    else:  
        opening_date = fake.date_between(start_date=min_opening, end_date=today)
        days_since_opening = (today - opening_date).days
        
        if status == 'Frozen':
            if days_since_opening >= 30:
                last_transaction = fake.date_between(
                    start_date=opening_date + timedelta(days=30),
                    end_date=today
                )
            else:
                if days_since_opening > 1:
                    last_transaction = fake.date_between(
                        start_date=opening_date,
                        end_date=today
                    )
                else:
                    last_transaction = opening_date
        else:  # Open
            # Recent activity (last 90 days)
            last_transaction = fake.date_between(
                start_date=today - timedelta(days=min(90, days_since_opening)),
                end_date=today
            )
    
    return opening_date, last_transaction

def generate_accounts(num_accounts, customer_ids, customer_birth_dates):
    conn = mysql.connector.connect(
        host='localhost', 
        user='root', 
        password='123456789Laz!', 
        database='banking'
    )
    cursor = conn.cursor()
    
    insert_sql = """
    INSERT INTO accounts (
        account_id, customer_id, balance, opening_date,
        account_type, account_status, overdraft_limit,
        last_transaction_date, interest_rate
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    fake = Faker()
    fake.unique.clear()
    
    accounts_per_customer = {}
    
    for i in range(num_accounts):
        idx = random.randint(0, len(customer_ids) - 1)
        customer_id = customer_ids[idx]
        customer_birth_date = customer_birth_dates[idx]
        
        if customer_id not in accounts_per_customer:
            accounts_per_customer[customer_id] = 0
        
        if accounts_per_customer[customer_id] == 0:
            account_type = random.choices(
                ['Checking', 'Savings', 'Money Market', 'CD'],
                weights=[60, 30, 5, 5]
            )[0]
        else:
            account_type = random.choices(
                ['Checking', 'Savings', 'Money Market', 'CD', 'Loan'],
                weights=[20, 30, 20, 15, 15]
            )[0]
        
        account_status = random.choices(
            ['Open', 'Closed', 'Frozen'],
            weights=[85, 10, 5]
        )[0]
        
        opening_date, last_transaction = date_check(account_status, customer_birth_date)
        
        balance = round(balance_check(account_type, account_status), 2)
        overdraft_limit = round(overdraft_check(account_type), 2)
        interest_rate = round(interest_check(account_type, account_status), 3)
        
        if account_status == 'Closed':
            last_transaction = None
        
        cursor.execute(insert_sql, (
            str(uuid4()),
            customer_id,
            balance,
            opening_date,
            account_type,
            account_status,
            overdraft_limit,
            last_transaction,
            interest_rate
        ))
        
        accounts_per_customer[customer_id] += 1
        
    
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":

    generate_accounts(10000, customer_ids, customer_birth_dates)
