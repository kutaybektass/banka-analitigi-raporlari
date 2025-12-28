from faker import Faker 
import mysql.connector
import random
from datetime import date, timedelta
from uuid import uuid4

def credit_score_by_tier(tier):
    if tier == 'Basic':
        return random.randint(300, 649)
    elif tier == 'Premium':
        return random.randint(650, 749)
    else:
        return random.randint(750, 850)

def join_date_check(birth_date):
    min_join = birth_date + timedelta(days= 18*365)
    max_join = date.today()
    return fake.date_between(min_join, max_join)

fake = Faker('en_US')
fake.unique.clear()

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="banking"
)
cursor = conn.cursor()

insert_sql = """
INSERT INTO customers (
    customer_id,
    first_name,
    last_name,
    email,
    phone,
    birth_date,
    address,
    city,
    state,
    zip_code,
    country,
    join_date,
    credit_score,
    customer_tier
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""


for i in range(5000):

    tier = random.choices(["Basic", "Premium", "VIP"], weights=[70, 25, 5])[0]

    birth_date = fake.date_of_birth(minimum_age=18, maximum_age=85)

    join_date = join_date_check(birth_date)
    ids = str(uuid4())

    cursor.execute(insert_sql, (
        ids,
        fake.first_name(),
        fake.last_name(),
        fake.unique.email(),
        fake.phone_number()[:18],
        birth_date,
        fake.street_address(),
        fake.city(),
        fake.state_abbr(),
        fake.zipcode(),
        'USA',
        join_date,
        credit_score_by_tier(tier),
        tier
    ))

conn.commit()
cursor.close()
conn.close()
