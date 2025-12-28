import random
from faker import Faker
from datetime import date, timedelta, datetime
import mysql.connector
from uuid import uuid4


fake = Faker()
fake.unique.clear()

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456789Laz!",
    database="banking"
)

cursor = conn.cursor()

account_ids = []
opening_dates = []
cursor.execute('SELECT account_id, opening_date FROM accounts;')
for i, j in cursor.fetchall():
    account_ids.append(i)
    opening_dates.append(j)

def date_check(opening_dates):
    dates = []
    for i in opening_dates:
        j = fake.date_time_between(start_date= i +timedelta(days = 1), end_date= datetime.now())
        if j.date() > i:
            dates.append(j)
    return dates
        
def time_check(opening_dates):
    dates_final = date_check(opening_dates)
    return [f"{k.date()} {random.randint(0,23):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}" for k in dates_final]
    
transaction_templates = [
    "Payment for {merchant}",
    "Purchase at {merchant}",
    "Online payment to {merchant}",
    "Refund from {merchant}",
    "Subscription charge for {service}",
    "Transfer to {person}",
    "Transfer from {person}",
    "ATM withdrawal",
    "Card payment at {merchant}",
]

def transaction_description():
    template = random.choice(transaction_templates)
    return template.format(
        merchant=fake.company(),
        service=fake.bs(),
        person=fake.name()
    )


insert_sql = """
INSERT INTO transactions(
    transaction_id,
    account_id,
    transaction_type,
    amount,
    transaction_timestamp,
    description,
    merchant_name,
    merchant_category,
    status,
    balance_after
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
all_timestamps = time_check(opening_dates * 2)


for i in range(7500):
    idx = random.randint(0, len(account_ids) - 1)
    account_id = account_ids[idx]
    opening_date = opening_dates[idx]

    days_after = random.randint(1, 365)  
    transaction_date = opening_date + timedelta(days=days_after)
    
    transaction_timestamp = f"{transaction_date} {random.randint(0,23):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}"
    
    cursor.execute(insert_sql, (
        str(uuid4()),
        account_id,  
        random.choices(['Deposit', 'Withdrawal', 'Transfer', 'Payment', 'Fee'], weights=[25, 25, 15, 30, 5])[0],
        random.triangular(1000, 20000, 7500),
        transaction_timestamp,
        transaction_description(),
        fake.name(),
        fake.bs(),
        random.choices(['Pending', 'Cancelled', 'Failed', 'Completed'], weights=[25, 25, 25, 25])[0],
        random.triangular(500, 10000, 3250)
    ))
    
conn.commit()
cursor.close()
conn.close()

