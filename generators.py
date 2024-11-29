import random
import datetime
from faker.proxy import Faker

gen = Faker()
import pg8000.native
con = pg8000.native.Connection("postgres", password="123123")



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
    x = int(datetime.datetime.now().timestamp())
    return str(datetime.datetime.fromtimestamp(random.randint(x, x + 1000000000)))


def gen_time_start_expected_end():
    x = random.randint(946674001, 1732894819)
    a = random.randint(x, x + 3600 * 4)
    b = random.randint(x - 3600 * 4, x)
    c = random.randint(b, a + int(3600 * 2.5))
    return [str(datetime.datetime.fromtimestamp(b)), str(datetime.datetime.fromtimestamp(c)), str(datetime.datetime.fromtimestamp(a))]


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


def insert(table, *args):
    l = len(args)
    fields = ''
    valeus = ''
    for i in range(l // 2):
        fields += f"{args[i]},"
    for i in range(l // 2, l):
        if type(args[i]) == str:
            valeus += f"'{args[i]}',"
        else:
            valeus += f"{args[i]},"
    con.run(f"INSERT INTO yandex_eats_ph.{table} ({fields[:-1]}) VALUES ({valeus[:-1]})")