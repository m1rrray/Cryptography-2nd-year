import math
import random


def pollards_rho(n, iterations_limit=10000):
    if n % 2 == 0:
        return 2
    x = random.randint(2, n - 1)
    y = x
    c = random.randint(1, n - 1)
    g = 1
    f = lambda x: (x * x + c) % n
    iterations = 0
    while g == 1 and iterations < iterations_limit:
        x = f(x)
        y = f(f(y))
        g = math.gcd(abs(x - y), n)
        iterations += 1
    return g if g != n else None


p = 100003
q = 100019
n = p * q

factor = pollards_rho(n)
if factor:
    print("Найденный делитель:", factor)
    print("Другой множитель:", n // factor)
else:
    print("Метод не нашёл нетривиальных делителей в заданном лимите итераций.")
