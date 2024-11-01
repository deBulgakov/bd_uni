import pg8000.native
from generators import Gen
import random

con = pg8000.native.Connection("postgres", password="123123")

with open('names.txt', 'r') as names, open('surnames1.txt', 'r') as surnames, open('cities.txt', 'r') as cities, open(
        'addresses.txt', 'r') as addresses:
    names = names.readlines()
    surnames = surnames.readlines()
    cities = cities.readlines()
    addresses = addresses.readlines()
    gen = Gen()
    #Generate main data
    for _ in range(10 ** 3):
        con.run(
            f'''INSERT INTO yandex_eats_ph.person (phone_number, full_name, login, password) VALUES ({gen.gen_phone_number()},'{gen.gen_fullname(names, surnames)}','{gen.gen_seq()}', '{gen.gen_pass()}')''')


    #Generate additional data
    for _ in range(10 ** 3):
        con.run(
            f"INSERT INTO yandex_eats_ph.address (city, street, house, entrance) VALUES ('{gen.gen_city(cities)}',  '{gen.gen_address(addresses)}','{gen.gen_number(2)}', {gen.gen_number(2)})")


    #Fill relations
    user_ids = con.run(f"SELECT person_id FROM yandex_eats_ph.person")
    address_ids = con.run(f"SELECT address_id FROM yandex_eats_ph.address")
    for user_id in user_ids:
        con.run(f"insert into yandex_eats_ph.change_address (person_id, address_id) values ({user_id[0]}, {random.choice(address_ids)[0]})")

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
