import datetime
from trace import Trace

import pg8000.native
from faker.proxy import Faker
import random
from generators import *

con = pg8000.native.Connection("postgres", password="123123")

# insert функция - ШУТКА! Все и без нее работает (con.run)

gen = Faker()
transport = ['On_foot', 'Bicycle', 'Car', 'Helicopter']
x = 1731500000

for _ in range(10 ** 3):
    insert('person',
           'phone_number', 'full_name', 'login', 'password',
           gen_phone_number(), gen.name(), gen.aba(), gen.aba().__hash__())
    insert('address',
           'city', 'street', 'house', 'entrance',
           gen.city(), gen_address(), gen_num(2), gen_num(2))
    insert('courier',
           'name', 'rating', 'transport', 'is_busy', 'gender',
           gen.name(), gen_rating(), random.choice(transport), random.choice([True, False]), gen_gender())
    insert('provider',
           'name', 'price_range', 'rating', 'contacts',
           gen_restaurant(), random.choice([1, 2, 3]), gen_rating(), gen_phone_number())
    insert('prov_address',
           'city', 'street', 'is_available',
           gen.city(), gen_address(), random.choice((True, False)))

person_ids = con.run(f"SELECT person_id FROM yandex_eats_ph.person")
address_ids = con.run(f"SELECT address_id FROM yandex_eats_ph.address")
provider_ids = con.run(f"SELECT provider_id FROM yandex_eats_ph.provider")
courier_ids = con.run(f"SELECT courier_id FROM yandex_eats_ph.courier")
provider_address_ids = con.run(f"SELECT prov_address_id FROM yandex_eats_ph.prov_address")

for person_id in person_ids:
    insert('change_address',
           'person_id', 'address_id',
           person_id[0], random.choice(address_ids)[0])
    insert('account',
           'person_id', 'points', 'promos', 'money_sum',
           person_id[0], gen_num(random.randint(1, 6)), gen.text(), random.randint(1, 1000000))

payments_ids = con.run(f'select payment_id from yandex_eats_ph.account')

for _ in range(10 ** 3):
    payment_id = random.choice(payments_ids)[0]
    provider_id = random.choice(provider_ids)[0]
    person = random.choice(person_ids)[0]
    provider = random.choice(provider_ids)[0]
    courier = random.choice(courier_ids)[0]
    time = gen_time_start_expected_end()
    insert('payment_info',
           'payment_id', 'card_number', 'cvc', 'exp_date', 'owner', 'bank',
           payment_id, gen_num(8), gen_num(3), gen_exp_date(), gen.name(), gen_bank())
    insert('dishes',
           'provider_id', 'nutrients_cfp', 'portion_size', 'contains', 'is_vegan',
           provider_id, gen_cfp(), gen_num(3), gen_contains(), random.choice([True, False]))
    insert('order',
           'person_id', 'provider_id', 'courier_id', 'data', 'datetime_start', 'datetime_expected', 'datetime_end',
           'price',
           person, provider, courier, gen.text(), time[0], time[1], time[2], random.randint(1, 1000000))

order_ids = con.run(f"SELECT order_id FROM yandex_eats_ph.order")
dish_ids = con.run(f"SELECT dish_id FROM yandex_eats_ph.dishes")

b = set()
a = set()
for _ in range(10 ** 3):
    dish = random.choice(dish_ids)[0]
    order = random.choice(order_ids)[0]
    b.add((order, dish))
    provider_address = random.choice(provider_address_ids)[0]
    provider = random.choice(provider_ids)[0]
    a.add((provider, provider_address))

for i in b:
    con.run(
        f"INSERT INTO yandex_eats_ph.order_dishes (order_id, dish_id) VALUES ({i[0]}, {i[1]})")

for i in a:
    con.run(
        f"INSERT INTO yandex_eats_ph.provider_prov_address (provider_id, prov_address_id) VALUES ({i[0]}, {i[1]})")

con.close()
