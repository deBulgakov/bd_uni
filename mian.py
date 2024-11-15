import datetime
import pg8000.native
from faker.proxy import Faker
import random


def gen_phone_number():
    return int(gen.basic_phone_number().replace('-', '').replace('(', '').replace(')', ''))


def gen_rating():
    return int(float(gen.numerify('#.##')) % 5 * 100) / 100


def gen_num(x):
    return gen.numerify('%' * x)

def gen_bank():
    return gen.name_male().split()[0] + 'Sachs Bank'

def gen_restaurant():
    return gen.company()+' '+random.choice(['Foods', 'Eats', 'Shwarma', 'King', 'I tochka'])

con = pg8000.native.Connection("postgres", password="123123")

gen = Faker()
transport = ['On_foot', 'Bicycle', 'Car', 'Helicopter']
x = 1731500000
# Generate main data
for _ in range(10 ** 3):
    con.run(
        f'''INSERT INTO yandex_eats_ph.person (phone_number, full_name, login, password) VALUES ({gen_phone_number()},'{gen.name()}','{gen.aba()}', '{gen.aba().__hash__()}')''')

# Generate additional data


for _ in range(10 ** 3):
    con.run(
        f"INSERT INTO yandex_eats_ph.address (city, street, house, entrance) VALUES ('{gen.city()}',  '{gen.address().replace('\n', ' ')}','{gen_num(2)}', {gen_num(2)})")
    con.run(
        f"INSERT INTO yandex_eats_ph.courier (name, rating, transport, is_busy) VALUES ('{gen.name()}',  {gen_rating()},'{random.choice(transport)}', {random.choice([True, False])})")
    con.run(
        f"INSERT INTO yandex_eats_ph.provider (name, price_range, rating, contacts) VALUES ('{gen_restaurant()}',  {random.choice([1, 2, 3])},{gen_rating()}, {gen_phone_number()})")

# Fill relations


person_ids = con.run(f"SELECT person_id FROM yandex_eats_ph.person")
address_ids = con.run(f"SELECT address_id FROM yandex_eats_ph.address")

for person_id in person_ids:
    con.run(
        f"insert into yandex_eats_ph.change_address (person_id, address_id) values ({person_id[0]}, {random.choice(address_ids)[0]})")
    con.run(
        f"INSERT INTO yandex_eats_ph.account (person_id, points, promos, money_sum) VALUES ('{person_id[0]}',  {gen_num(random.randint(1, 6))},'{gen.text()}', {random.randint(1, 1000000)})")

payments_ids = con.run(f'select payment_id from yandex_eats_ph.account')
for payment in payments_ids:
    con.run(
        f"INSERT INTO yandex_eats_ph.payment_info (payment_id, card_number, cvc, exp_date, owner, bank) VALUES ({payment[0]},{gen_num(8)},'{gen_num(3)}', '{datetime.datetime.fromtimestamp(random.randint(x, x + 1000000000))}', '{gen.name()}', '{gen_bank()}')")

con.close()
