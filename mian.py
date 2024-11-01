import random
import pg8000.native
import re
from scripts import create_script

con = pg8000.native.Connection("postgres", password="123123")


# Create a temporary table


# con.run(create_script)

# Populate the table

def gen_phone_number():
    alph = '1234567890'
    number = '+7'
    for i in range(10):
        number += random.choice(alph)
    return number


def gen_fullname(t, t2):
    name = random.choice(t)[:-1]
    surname = random.choice(t2)[:-1]
    return str(name + ' ' + surname)


def gen_city(t):
    city = random.choice(t)[:-1]
    return city


def gen_seq():
    alph = 'qwertyuiopasdfghjklzxcvbnm1234567890 '
    seq = ''
    for i in range(random.randint(5, 15)):
        seq += random.choice(alph)
    return seq


with open('names.txt', 'r') as f, open('surnames1.txt', 'r') as f2, open('cities.txt', 'r') as f3:
    f = f.readlines()
    f2 = f2.readlines()
    f3 = f3.readlines()
    for i in range(10 ** 3):
        con.run(
            f"INSERT INTO yandex_eats_ph.person (phone_number, full_name, login) VALUES ({gen_phone_number()},'{gen_fullname(f, f2)}','{gen_seq()}')")
        # con.run(f"-- INSERT INTO yandex_eats_ph.courier (name) VALUES ('biba')")
        con.run(f"INSERT INTO yandex_eats_ph.address (city) VALUES ('{gen_city(f3)}')")

# Print all the rows in the table

# for row in con.run("SELECT * FROM yandex_eats_ph.person"):
#     print('person', row)
for row in con.run("SELECT * FROM yandex_eats_ph.address"):
    print('address', row)
# for row in con.run("SELECT * FROM yandex_eats_ph.address"):
#     print('address', row)

con.close()
