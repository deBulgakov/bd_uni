import pg8000.native
from faker.proxy import Faker

from generators import Gen
import random
import faker

con = pg8000.native.Connection("postgres", password="123123")

gen = Faker()
transport = ['On_foot', 'Bicycle', 'Car', 'Helicopter']
# Generate main data
for _ in range(10 ** 3):
    con.run(
        f'''INSERT INTO yandex_eats_ph.person (phone_number, full_name, login, password) VALUES ({int(gen.basic_phone_number().replace('-', '').replace('(', '').replace(')', ''))},'{gen.name()}','{gen.aba()}', '{gen.aba().__hash__()}')''')


# Generate additional data


for _ in range(10 ** 3):
    con.run(
        f"INSERT INTO yandex_eats_ph.address (city, street, house, entrance) VALUES ('{gen.city()}',  '{gen.address().replace('\n', ' ')}','{gen.numerify('%%')}', {gen.numerify('%%')})")
    con.run(
        f"INSERT INTO yandex_eats_ph.courier (name, rating, transport, is_busy) VALUES ('{gen.name()}',  {float(gen.numerify('#.##')) % 5},'{random.choice(transport)}', {random.choice([True, False])})")

# Fill relations


user_ids = con.run(f"SELECT person_id FROM yandex_eats_ph.person")
address_ids = con.run(f"SELECT address_id FROM yandex_eats_ph.address")
for user_id in user_ids:
    con.run(
        f"insert into yandex_eats_ph.change_address (person_id, address_id) values ({user_id[0]}, {random.choice(address_ids)[0]})")




n = 10
for row in con.run(f"SELECT * FROM yandex_eats_ph.person limit {n}"):
    print('person', row)
for row in con.run(f"SELECT * FROM yandex_eats_ph.address limit {n}"):
    print('address', row)
for row in con.run(f"SELECT * FROM yandex_eats_ph.change_address limit {n}"):
    print('change_address', row)
# for row in con.run("SELECT * FROM yandex_eats_ph.address"):
#     print('address', row)

con.close()
