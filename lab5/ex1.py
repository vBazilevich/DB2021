from faker import Faker
import psycopg2
import sys
import random

# CONSTANTS secion
DB = 'lab5'
USER = 'python_user'
PASS = 'password'
HOST = '127.0.0.1'
PORT = '5432'
CUSTOMERS = 100000
CREATE_BTREE_INDEX = True
CREATE_HASH_INDEX = True

print('Establishing connection to database...')
try:
    con = psycopg2.connect(database = DB, user = USER, password = PASS, host = HOST, port = PORT)
except psycopg2.Error as e:
    print(e.pgcode)
    print(e.pgerror)
    exit(-1)
else:
    print('Connection established.')

cursor = con.cursor()

print('Creating table customers')
try:
    cursor.execute('DROP TABLE IF EXISTS customers;')
    cursor.execute(''' CREATE TABLE customers
                    (ID SERIAL PRIMARY KEY,
                     NAME TEXT NOT NULL,
                     ADDRESS TEXT NOT NULL,
                     AGE INT NOT NULL,
                     REVIEW TEXT NOT NULL);''')
    if CREATE_BTREE_INDEX:
        cursor.execute('CREATE INDEX age_index ON customers (AGE);')
    if CREATE_HASH_INDEX:
        cursor.execute('CREATE INDEX name_index ON customers USING hash (NAME);')
    con.commit()
except psycopg2.Error as e:
    print(e.pgcode)
    print(e.pgerror)
    exit(-1)
else:
    print('Table customers is created')

fake = Faker()
def insert_random_customer(cursor):
    name = fake.name()
    address = fake.address()
    age = random.randint(0, 100)
    review = fake.text(max_nb_chars=100)
    try:
        cursor.execute(f"INSERT INTO customers (NAME, ADDRESS, AGE, REVIEW) VALUES ('{name}', '{address}', {age}, '{review}');")
    except psycopg2.Error as e:
        print(e.pgcode)
        print(e.pgerror)
        exit(-1)

print(f"Instantiating table with {CUSTOMERS} customers")
for _ in range(CUSTOMERS):
    insert_random_customer(cursor)

try:
    con.commit()
except psycopg2.Error as e:
    print(e.pgcode)
    print(e.pgerror)
    exit(-1)
else:
    print('Database instantiated successfully.')

print("Adding special customer for testing hash index")
try:
    cursor.execute("INSERT INTO customers (NAME, ADDRESS, AGE, REVIEW) VALUES ('Vlad Minkin', 'Russia, Tatarstan', 42, 'Good job!');")
    con.commit()
except psycopg2.Error as e:
    print(e.pgcode)
    print(e.pgerror)
    exit(-1)

print("Here is report for range test(B-tree index on age):")
try:
    cursor.execute("EXPLAIN ANALYSE SELECT * FROM customers WHERE AGE > 20 and AGE < 40;")
    for row in cursor.fetchall():
        print(row)
except psycopg2.Error as e:
    print(e.pgcode)
    print(e.pgerror)

print("Here is report for equality test(hash index on name):")
try:
    cursor.execute("EXPLAIN ANALYSE SELECT * FROM customers WHERE NAME = 'Vlad Minkin';")
    for row in cursor.fetchall():
        print(row)
except psycopg2.Error as e:
    print(e.pgcode)
    print(e.pgerror)

con.close()
