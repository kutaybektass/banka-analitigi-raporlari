import random
from faker import Faker
from uuid import uuid4
import mysql.connector
from datetime import date, datetime, timedelta


fake = Faker()
fake.unique.clear()


conn = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'banking'
    )

cursor = conn.cursor()
customers = []
cursor.execute("SELECT customer_id FROM customers;")
for i in cursor.fetchall():
    customers.append(i[0])


loan_accounts_dates = []
cursor.execute("SELECT opening_date FROM accounts WHERE account_type = 'Loan'")
for j in cursor.fetchall():
    loan_accounts_dates.append(j[0])


def start_date_check(loan_accounts_dates):
    start_dates = []
    for i in loan_accounts_dates:
        while True:
            j = fake.date_time_between(start_date= i + timedelta(days= 1), end_date= datetime.now())
            if j.date() > i and j.date() >= date(2000, 1, 1):
                start_dates.append(j)
                break
    return start_dates

def monthly_payment_check(loan_amount, annual_interest_percent, term_months):
    monthly_rate = (annual_interest_percent / 100) / 12
    
    if monthly_rate == 0:
        return loan_amount / term_months
    
    numerator = monthly_rate * ((1 + monthly_rate) ** term_months)
    denominator = ((1 + monthly_rate) ** term_months) - 1
    
    monthly_payment = loan_amount * (numerator / denominator)
    return monthly_payment


def remaining_balance_check(status, loan_amount, interest_rate, term_months):
    monthly_payment = monthly_payment_check(loan_amount, interest_rate, term_months)
    if status =='Paid Off':
        return 0.00
    if status in ['Delinquent', 'Defaulted']:
        payments_made = random.randint(0, term_months // 2)  
    else:  
        payments_made = random.randint(1, term_months - 1)
    
    remaining_balance = loan_amount -  (monthly_payment * payments_made)
    return round(max(0.00, remaining_balance), 2)

collateral_templates = [
    "Residential property at {address} - {square_feet} sq ft, built {year}",
    "Commercial property: {property_type} at {address}, {square_feet} sq ft",
    "Vehicle: {year} {make} {model}, VIN: {vin}, {mileage} miles",
    "Investment portfolio: {securities_type} valued at ${amount}",
    "Certificate of Deposit: ${amount} at {bank_name}, maturing {date}",
    "Savings account: ${amount} at {bank_name}, account #{account}",
    "Stock collateral: {shares} shares of {company} ({ticker})",
    "Business equipment: {equipment_type}, serial #{serial}",
    "Jewelry: {item_type}, appraised value ${amount}, {details}",
    "Artwork: '{title}' by {artist}, appraised ${amount}",
    "Unsecured personal loan - credit based",
    "Blanket lien on business assets",
    "Timeshare: {location}, week {week_number}, unit {unit}",
    "Boat: {year} {make} {model}, {length}ft, hull #{hull}",
    "Aircraft: {year} {make} {model}, tail #{tail_number}",
]

def generate_collateral(collateral_templates):
    template = random.choice(collateral_templates)
    
    # Fill template with realistic data
    replacements = {
        'address': fake.street_address() + ", " + fake.city() + ", " + fake.state_abbr(),
        'square_feet': random.choice(["1,200", "1,800", "2,400", "3,000", "5,000"]),
        'year': str(random.randint(1990, 2023)),
        'property_type': random.choice(["office building", "retail space", "warehouse", "apartment complex"]),
        'make': random.choice(["Toyota", "Honda", "Ford", "Chevrolet", "BMW", "Mercedes"]),
        'model': random.choice(["Camry", "Accord", "F-150", "Silverado", "3 Series", "C-Class"]),
        'vin': fake.vin(),
        'mileage': f"{random.randint(5000, 150000):,}",
        'securities_type': random.choice(["mutual funds", "ETFs", "bonds", "blue-chip stocks"]),
        'amount': f"{random.randint(10000, 500000):,}",
        'bank_name': fake.company(),
        'date': fake.date_between(start_date='+1y', end_date='+5y').strftime('%m/%d/%Y'),
        'account': fake.bban(),
        'shares': random.randint(100, 10000),
        'company': fake.company(),
        'ticker': fake.lexify(text='???').upper(),
        'equipment_type': random.choice(["construction equipment", "medical devices", "manufacturing machinery", "IT hardware"]),
        'serial': fake.ean13(),
        'item_type': random.choice(["diamond ring", "gold necklace", "watch collection", "bracelet"]),
        'details': random.choice(["with certification", "family heirloom", "recent appraisal"]),
        'title': fake.catch_phrase().title(),
        'artist': fake.name(),
        'location': fake.city() + ", " + fake.country(),
        'week_number': random.randint(1, 52),
        'unit': random.randint(100, 999),
        'length': random.choice(["22", "30", "42", "50"]),
        'hull': fake.bothify(text='??####').upper(),
        'tail_number': fake.bothify(text='N#####').upper(),
    }
    
    for key, value in replacements.items():
        placeholder = '{' + key + '}'
        if placeholder in template:
            template = template.replace(placeholder, str(value))
    
    return template


insert_sql = """
INSERT INTO loans(
    loan_id,
    customer_id,
    loan_amount,
    interest_rate,
    term_months,
    start_date,
    monthly_payment,
    remaining_balance,
    collateral_description,
    status
)
VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

all_start_dates = start_date_check(loan_accounts_dates)

for i in range(1000):
    
    status = random.choices(['Active', 'Delinquent', 'Paid Off', 'Defaulted'], weights= [25, 25, 25, 25])[0]

    interest_rate = random.uniform(3.000, 18.000)

    term_months = random.choices([12, 24, 36, 48, 60], weights = [20, 20, 20, 20, 20])[0]

    loan_amount = random.choices([1000, 5000, 10000, 20000, 50000, 100000, 200000], weights=[15, 20, 20, 15, 15, 10, 5])[0]

    cursor.execute(insert_sql, (
        str(uuid4()),
        random.choice(customers),
        loan_amount,
        interest_rate,
        term_months,
        random.choice(all_start_dates),
        round(monthly_payment_check(loan_amount, interest_rate, term_months), 2),
        remaining_balance_check(status, loan_amount, interest_rate, term_months),
        generate_collateral(collateral_templates),
        status
    ))


conn.commit()
cursor.close()
conn.close()