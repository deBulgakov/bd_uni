import base64
import random


class Gen:
    def __init__(self):
        pass

    def gen_number(self, l=10):
        number = ''
        for _ in range(l):
            number += str(random.randint(0, 10))
        return number

    def gen_phone_number(self):
        number = '+7' + str(self.gen_number(10))
        return number

    def gen_fullname(self, t, t2):
        name = random.choice(t)[:-1]
        surname = random.choice(t2)[:-1]
        return str(name + ' ' + surname)

    def gen_city(self, t):
        city = random.choice(t)[:-1]
        return city

    def gen_seq(self, l=random.randint(5, 15)):
        alph = 'qwertyuiopasdfghjklzxcvbnm1234567890 '
        seq = ''
        for _ in range(l):
            seq += random.choice(alph)
        return seq

    def gen_pass(self):
        a = self.gen_seq(30)
        return str(base64.b64encode(a.encode("utf-8")))[2:-1]

    def gen_address(self, f):
        return random.choice(f)[:-1]


