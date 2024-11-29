import datetime
from trace import Trace

import pg8000.native
from faker.proxy import Faker
import random


def gen_phone_number():
    return int(gen.basic_phone_number().replace('-', '').replace('(', '').replace(')', ''))


def gen_gender():
    return random.choice(('Male', 'Female', 'Gachi_Boss', 'Dungeon_master', 'AH-64 Apache', 'Ryba', 'Toyota'))


def gen_rating():
    return int(float(gen.numerify('#.##')) % 5 * 100) / 100


def gen_address():
    return gen.address().replace('\n', ' ')


def gen_num(x):
    return gen.numerify('%' * x)


def gen_bank():
    return gen.name_male().split()[0] + 'Sachs Bank'


def gen_restaurant():
    return gen.company() + ' ' + random.choice(['Foods', 'Eats', 'Shwarma', 'King', 'I tochka'])


def gen_exp_date():
    return datetime.datetime.fromtimestamp(random.randint(x, x + 1000000000))


def gen_time_start_expected_end():
    x = random.randint(946674001, 1732894819)
    a = random.randint(x, x + 3600 * 4)
    b = random.randint(x - 3600 * 4, x)
    c = random.randint(b, a + int(3600 * 2.5))
    return [datetime.datetime.fromtimestamp(b), datetime.datetime.fromtimestamp(c), datetime.datetime.fromtimestamp(a)]


def gen_cfp():
    su = 100
    carbs = random.randint(1, 50)
    fats = random.randint(1, 50)
    proteins = su - carbs - fats
    return (carbs, fats, proteins)


def gen_contains():
    a = ['соль', 'куриные яйца', 'сахар', 'растительное масло', 'пшеничная мука', 'чёрный перец', 'сливочное масло',
         'лук', 'морковь',
         'картофель', 'помидоры', 'различные виды зелени', 'сладкий перец', 'яблоки', 'лимоны', 'томатная паста',
         'куриное филе',
         'капуста', 'сыр', 'мёд', 'сухофрукты', 'орехи и семечки', ]
    s = ''
    for _ in range(random.randint(3, 7)):
        s += random.choice(a) + ', '
    return s[:-2]


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
        f"INSERT INTO yandex_eats_ph.address (city, street, house, entrance) VALUES ('{gen.city()}',  '{gen_address()}','{gen_num(2)}', {gen_num(2)})")
    con.run(
        f"INSERT INTO yandex_eats_ph.courier (name, rating, transport, is_busy, gender) VALUES ('{gen.name()}',  {gen_rating()},'{random.choice(transport)}', {random.choice([True, False])}, '{gen_gender()}')")
    con.run(
        f"INSERT INTO yandex_eats_ph.provider (name, price_range, rating, contacts) VALUES ('{gen_restaurant()}',  {random.choice([1, 2, 3])},{gen_rating()}, {gen_phone_number()})")
    con.run(
        f"INSERT INTO yandex_eats_ph.prov_address (city, street, is_available) VALUES ('{gen.city()}', '{gen_address()}', {random.choice((True, False))})")

# Fill relations
person_ids = con.run(f"SELECT person_id FROM yandex_eats_ph.person")
address_ids = con.run(f"SELECT address_id FROM yandex_eats_ph.address")
provider_ids = con.run(f"SELECT provider_id FROM yandex_eats_ph.provider")
courier_ids = con.run(f"SELECT courier_id FROM yandex_eats_ph.courier")
provider_address_ids = con.run(f"SELECT prov_address_id FROM yandex_eats_ph.prov_address")

for person_id in person_ids:
    con.run(
        f"insert into yandex_eats_ph.change_address (person_id, address_id) values ({person_id[0]}, {random.choice(address_ids)[0]})")
    con.run(
        f"INSERT INTO yandex_eats_ph.account (person_id, points, promos, money_sum) VALUES ('{person_id[0]}',  {gen_num(random.randint(1, 6))},'{gen.text()}', {random.randint(1, 1000000)})")

payments_ids = con.run(f'select payment_id from yandex_eats_ph.account')

for _ in range(10):
    payment_id = random.choice(payments_ids)[0]
    con.run(
        f"INSERT INTO yandex_eats_ph.payment_info (payment_id, card_number, cvc, exp_date, owner, bank) VALUES ({payment_id},{gen_num(8)},'{gen_num(3)}', '{gen_exp_date()}', '{gen.name()}', '{gen_bank()}')")

for _ in range(10):
    provider_id = random.choice(provider_ids)[0]
    con.run(
        f"INSERT INTO yandex_eats_ph.dishes (provider_id, nutrients_cfp,portion_size, contains, is_vegan) VALUES ({provider_id}, {gen_cfp()},{gen_num(3)} ,'{gen_contains()}', {random.choice([True, False])})")

dish_ids = con.run(f"SELECT dish_id FROM yandex_eats_ph.dishes")

# Order
for _ in range(10):
    person = random.choice(person_ids)[0]
    provider = random.choice(provider_ids)[0]
    courier = random.choice(courier_ids)[0]
    time = gen_time_start_expected_end()
    con.run(
        f"INSERT INTO yandex_eats_ph.order (person_id, provider_id, courier_id, data, datetime_start, datetime_expected, datetime_end, price) VALUES ({person}, {provider}, {courier}, '{gen.text()}','{time[0]}','{time[1]}','{time[2]}', {random.randint(1, 1000000)})")

order_ids = con.run(f"SELECT order_id FROM yandex_eats_ph.order")

# Dishes
b = set()
for _ in range (10 ** 3):
    dish = random.choice(dish_ids)[0]
    order = random.choice(order_ids)[0]
    b.add((order, dish))

for i in b:
    con.run(
        f"INSERT INTO yandex_eats_ph.order_dishes (order_id, dish_id) VALUES ({i[0]}, {i[1]})")

# Provider_address
b = set()
for _ in range (10 ** 3):
    provider_address = random.choice(provider_address_ids)[0]
    provider = random.choice(provider_ids)[0]
    b.add((provider, provider_address))

for i in b:
    con.run(
        f"INSERT INTO yandex_eats_ph.provider_prov_address (provider_id, prov_address_id) VALUES ({i[0]}, {i[1]})")

con.close()
