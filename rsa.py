import random


class RSA:
    def __init__(self, p=None, q=None):
        if p and q:
            self.public_key, self.private_key = self.generate_keypair(p, q)
        else:
            self.public_key, self.private_key = (None, None)

    @staticmethod
    def gcd(a, b):
        """Находит НОД двух чисел"""
        while b != 0:
            a, b = b, a % b
        return a

    @staticmethod
    def mod_inverse(e, phi):
        """Находит мультипликативно обратное для e по модулю phi"""

        def egcd(a, b):
            if a == 0:
                return b, 0, 1
            else:
                g, y, x = egcd(b % a, a)
                return g, x - (b // a) * y, y

        g, x, y = egcd(e, phi)
        if g != 1:
            raise Exception('Мультипликативно обратного не существует')
        else:
            return x % phi

    @staticmethod
    def my_pow(base, exponent, modulus):
        """
        Вычисляет (base ** exponent) % modulus эффективным способом
        """
        if modulus == 1:
            return 0
        result = 1
        base = base % modulus
        while exponent > 0:
            if exponent % 2 == 1:
                result = (result * base) % modulus
            exponent = exponent >> 1
            base = (base * base) % modulus
        return result

    @staticmethod
    def generate_keypair(p, q):
        """Генерирует открытый и закрытый ключи"""
        n = p * q
        phi = (p - 1) * (q - 1)

        e = random.randrange(1, phi)
        while RSA.gcd(e, phi) != 1:
            e = random.randrange(1, phi)

        d = RSA.mod_inverse(e, phi)

        return (e, n), (d, n)

    def encrypt(self, plaintext):
        """Шифрует текст с использованием открытого ключа"""
        e, n = self.public_key
        # слово
        ciphertext = ' '.join([str(self.my_pow(ord(char), e, n)) for char in plaintext])
        # число
        # ciphertext = [self.my_pow(int(plaintext), e, n)]
        return ciphertext

    def decrypt(self, ciphertext):
        """Расшифровывает текст с использованием закрытого ключа"""
        d, n = self.private_key

        # слово
        plaintext = ''.join([chr(self.my_pow(char, d, n)) for char in ciphertext])
        # число
        # plaintext = ''.join([str(self.my_pow(char, d, n)) for char in ciphertext])
        return plaintext
