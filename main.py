from itertools import product

import numpy as np
from sympy import symbols, Poly, factor, divisors, factorint, div, simplify


class GaloisField:
    x = symbols('x')

    def __init__(self, p, n):
        self.p = p
        self.n = n
        self.elements = [i for i in range(p)]
        self.field = list(map(list, product(self.elements, repeat=self.n)))

    def polynomial_generator(self) -> list:
        """Генерирует многочлены, у которых в старшей степени коэффициент не ноль"""
        polynomials = product(range(self.p), repeat=self.n + 1)
        suitable = [poly for poly in polynomials if poly[0] != 0]

        return suitable

    def mobius(self, n):
        x = symbols('x')

        if n == 1:
            return 1

        factorization = factorint(n)
        k = len(factorization)

        if any(exp > 1 for exp in factorization.values()):
            return 0

        return (-1) ** k

    def evaluate_polynomial(self, poly: list) -> bool:
        """Проверяет многочлен на неприводимость"""
        x = symbols('x')
        for a in range(self.p):
            result = 0
            for i, coef in enumerate(reversed(poly)):
                result += coef * (a ** i)
            result %= self.p
            if result == 0:
                return False

        poly_new = Poly(poly, x)
        n = poly_new.degree()

        product = 1
        if n < 3:
            return True
        for d in divisors(n):
            a = (x ** (self.p ** (n // d)) - x) ** self.mobius(d)
            product *= a

        product = simplify(factor(product))
        product = Poly(product, x)

        return div(product, poly_new)[1] != 0

    def find_irreducible_polynomials(self) -> list:
        """Возвращает неприводимые многочлены"""
        x = symbols('x')
        irreducible_polynomials = []
        polynomials = self.polynomial_generator()
        k = 0
        for poly in polynomials:
            if self.evaluate_polynomial(poly):
                k += 1
                irreducible_polynomials.append(poly)

        return irreducible_polynomials

    # def find_degree(self, poly: list) -> list:
    #     """Находит x^n из неприводимого многочлена"""
    #     length = len(poly)
    #     first_part = poly[0]
    #
    #     if first_part == 1:
    #         return [-poly[i] % self.p for i in range(1, length)]
    #     else:
    #         new_poly = [-poly[i] % self.p for i in range(1, length)]
    #         ans = []
    #         for element in new_poly:
    #             n = 0
    #             dividend = (element + self.p * n) / first_part
    #             while int(dividend) - dividend != 0:
    #                 n += 1
    #                 dividend = (element + self.p * n) / first_part
    #             ans.append(int(dividend))
    #         return ans

    def __add__(self, poly1: list, poly2: list):
        """Реализует операцию сложения по модулю p"""
        poly1 = np.array(poly1)
        poly2 = np.array(poly2)
        return list((poly1 + poly2) % self.p)

    # def __mul__(self, poly1: list, poly2: list, irreducible_poly: list) -> list:
    #     """Реализует операцию умножения двух многочленов с помощью неприводимого многочлена"""
    #     x = symbols('x')
    #
    #     poly1_sym = Poly(poly1, x, domain='ZZ')
    #     poly2_sym = Poly(poly2, x, domain='ZZ')
    #
    #     result = (poly1_sym * poly2_sym).as_expr()
    #
    #     new_result = result.replace(x ** len(irreducible_poly), Poly(irreducible_poly, x, domain='ZZ').as_expr())
    #     new_result = Poly(new_result, x, domain='ZZ').all_coeffs()
    #     # plen = len(new_result)
    #     # if plen > 3:
    #     #     print(new_result, plen, poly1, poly2, irreducible_poly)
    #     #     while True:
    #     #         pass
    #
    #     new_result = abs((len(poly1)) - len(new_result)) * [0] + new_result
    #     # print(len(new_result))
    #     new_result = [element % self.p for element in new_result]
    #     return new_result

    def compute_element_orders(self, irr_poly):
        x = symbols('x')
        element_orders = {}
        n = 0
        for element in self.field[1:]:

            const_x = element.copy()
            order = 1
            current = self.__mul__(const_x, const_x, irr_poly)
            n += 1
            while current != element:
                current = self.__mul__(current, const_x, irr_poly)
                order += 1

            element_orders[tuple(element)] = order

        return element_orders

    def __mul__(self, polyforst, poly2, irr_poly):

        x = symbols('x')
        poly1 = Poly(polyforst, x)
        poly2 = Poly(poly2, x)
        res = (poly1 * poly2).all_coeffs()
        new_result = [element % self.p for element in res]
        new_result = Poly(new_result, x)
        irr_poly = Poly(irr_poly, x)
        new_result = div(new_result, irr_poly)[1].all_coeffs()
        new_result = abs((len(polyforst)) - len(new_result)) * [0] + new_result

        ans = []
        for element in new_result:

            n = 0
            if isinstance(element, int):
                ans.append(element % self.p)
            else:
                dividend = (element.p + self.p * n) * element.q
                while not isinstance(dividend, int):
                    n += 1
                    dividend = (element.p + self.p * n) / element.q
                dividend %= self.p
                ans.append(int(dividend))

        return ans

    def __str__(self):
        return str(list(map(list, product(self.elements, repeat=self.n))))


if __name__ == '__main__':
    x = symbols('x')
    p, n = int(input("Введите простое число p: ")), int(input("Введите натуральное число n: "))
    gf = GaloisField(p, n)

    print(f"Элементы поля: {[Poly(element, x, domain='ZZ').as_expr() for element in gf.field]}")
    irr_polys = gf.find_irreducible_polynomials()

    print(f'Неприводимые многочлены: {irr_polys}')
    print(f"Теперь выберите неприводимый многочлен с помощью цифры от 1 до {len(irr_polys)}")

    irr_index = int(input())
    selected_irr_poly = irr_polys[irr_index - 1]

    print(f"Выбранный неприводимый многочлен: {selected_irr_poly}")

    element_orders = gf.compute_element_orders(selected_irr_poly)  #

    print("Порядки элементов в поле Галуа:")
    primitives = []
    for element, order in element_orders.items():
        print(f"Элемент {Poly(element, x, domain='ZZ').as_expr()}: порядок {order}")
        if order == p ** n - 1:
            primitives.append(element)

    print("\nТеперь выберите образующий элемент для разложения по степеням из"
          f" {[Poly(element, x, domain='ZZ').as_expr() for element in primitives]}:")
    primitive_index = int(input(f"Введите номер элемента (от 1 до {len(primitives)}): "))
    primitive_element = primitives[primitive_index - 1]

    print(f"\nВыбранный образующий элемент: {Poly(primitive_element, x, domain='ZZ').as_expr()}")
    print("\nРазложение по степеням:")
    current = primitive_element
    for i in range(1, max(element_orders.values()) + 1):
        print(f"Степень {i}: {Poly(current, x, domain='ZZ').as_expr()}")
        current = gf.__mul__(current, list(primitive_element), selected_irr_poly)

    print('Теперь вы можете умножить 2 элемента из поля друг на друга')
    first_poly_mul = Poly(input('Введи первый полином в формате a1*x**n + a2*x**(n-1) ... an*x**0 : '), x, domain='ZZ')
    second_poly_mul = Poly(input('Введи второй полином в формате a1*x**n + a2*x**(n-1) ... an*x**0 : '), x, domain='ZZ')

    first_poly_mul = abs(gf.n - len(first_poly_mul.all_coeffs())) * [0] + first_poly_mul.all_coeffs()
    second_poly_mul = abs(gf.n - len(second_poly_mul.all_coeffs())) * [0] + second_poly_mul.all_coeffs()

    if first_poly_mul not in gf.field or second_poly_mul not in gf.field:
        raise ValueError('Введите многочлены из поля Галуа')
    mul_res_mul = gf.__mul__(first_poly_mul, second_poly_mul, selected_irr_poly)
    print(Poly(mul_res_mul, x, domain='ZZ').as_expr())

    print("Теперь вы можете сложить 2 элемента из поля галуа")
    first_poly_add = Poly(input('Введи первый полином в формате a1*x**n + a2*x**(n-1) ... an*x**0 : '), x, domain='ZZ')
    second_poly_add = Poly(input('Введи второй полином в формате a1*x**n + a2*x**(n-1) ... an*x**0 : '), x, domain='ZZ')

    first_poly_add = abs(gf.p - len(first_poly_add.all_coeffs()) - 1) * [0] + first_poly_add.all_coeffs()
    second_poly_add = abs(gf.p - len(second_poly_add.all_coeffs()) - 1) * [0] + second_poly_add.all_coeffs()

    if first_poly_add not in gf.field or second_poly_add not in gf.field:
        raise ValueError('Введите многочлены из поля Галуа')

    mul_res_add = gf.__add__(first_poly_add, second_poly_add)
    print(Poly(mul_res_add, x, domain='ZZ').as_expr())
