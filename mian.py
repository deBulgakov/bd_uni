import datetime
import pg8000.native
from faker.proxy import Faker
import random

con = pg8000.native.Connection("postgres", password="123123")

gen = Faker()
transport = ['On_foot', 'Bicycle', 'Car', 'Helicopter']
x = 1731500000
# Generate main data
for _ in range(10 ** 3):
    con.run(
        f'''INSERT INTO yandex_eats_ph.person (phone_number, full_name, login, password) VALUES ({int(gen.basic_phone_number().replace('-', '').replace('(', '').replace(')', ''))},'{gen.name()}','{gen.aba()}', '{gen.aba().__hash__()}')''')

# Generate additional data


for _ in range(10 ** 3):
    con.run(
        f"INSERT INTO yandex_eats_ph.address (city, street, house, entrance) VALUES ('{gen.city()}',  '{gen.address().replace('\n', ' ')}','{gen.numerify('%%')}', {gen.numerify('%%')})")
    con.run(
        f"INSERT INTO yandex_eats_ph.courier (name, rating, transport, is_busy) VALUES ('{gen.name()}',  {int(float(gen.numerify('#.##')) % 5 * 100) / 100},'{random.choice(transport)}', {random.choice([True, False])})")

# Fill relations


person_ids = con.run(f"SELECT person_id FROM yandex_eats_ph.person")
address_ids = con.run(f"SELECT address_id FROM yandex_eats_ph.address")

for person_id in person_ids:
    con.run(
        f"insert into yandex_eats_ph.change_address (person_id, address_id) values ({person_id[0]}, {random.choice(address_ids)[0]})")
    con.run(
        f"INSERT INTO yandex_eats_ph.account (person_id, points, promos, money_sum) VALUES ('{person_id[0]}',  {int(gen.numerify('%' * random.randint(1, 6)))},'{gen.text()}', {random.randint(1, 1000000)})")

payments_ids = con.run(f'select payment_id from yandex_eats_ph.account')
for payment in payments_ids:
    con.run(
        f"INSERT INTO yandex_eats_ph.payment_info (payment_id, card_number, cvc, exp_date, owner, bank) VALUES ({payment[0]},{int(gen.numerify('#' * 8))},'{int(gen.numerify('#' * 3))}', '{datetime.datetime.fromtimestamp(random.randint(x, x+ 1000000000))}', '{gen.name()}', '{gen.name_male().split()[0] + 'Sachs Bank'}')")


con.close()
