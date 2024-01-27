from itertools import product
import numpy as np
from sympy import symbols, Poly, factor, divisors, factorint, div, simplify


def mobius(n):
    """Реализация функции мебиуса для поиска неприводимого многочлена"""

    if n == 1:
        return 1

    factorization = factorint(n)
    k = len(factorization)

    if any(exp > 1 for exp in factorization.values()):
        return 0

    return (-1) ** k


class GaloisField:
    x = symbols('x')

    def __init__(self, p: int, n: int):
        self.p = p
        self.n = n
        self.elements = [k for k in range(p)]
        self.field = list(map(list, product(self.elements, repeat=self.n)))

    def polynomial_generator(self) -> list:
        """Генерирует многочлены, у которых в старшей степени коэффициент не ноль"""

        polynomials = product(range(self.p), repeat=self.n + 1)
        suitable = [poly for poly in polynomials if poly[0] != 0]

        return suitable

    def evaluate_polynomial(self, poly: list) -> bool:
        """Проверяет многочлен на неприводимость"""

        x_eval = symbols('x')
        poly_new = Poly(poly, x_eval)
        max_degree_poly = poly_new.degree()

        composition = 1
        for d in divisors(max_degree_poly):
            res_local_compose = (x_eval ** (self.p ** (max_degree_poly // d)) - x_eval) ** mobius(d)
            composition *= res_local_compose

        composition = simplify(factor(composition))
        composition = Poly(composition, x_eval)

        r = div(composition, poly_new)[1].all_coeffs()

        ans = []
        for element in r:

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

        return not sum(ans)

    def find_irreducible_polynomials(self) -> list:
        """Возвращает неприводимые многочлены"""

        irreducible_polynomials = []
        polynomials = self.polynomial_generator()
        k = 0
        for poly in polynomials:
            if self.evaluate_polynomial(poly):
                k += 1
                irreducible_polynomials.append(poly)

        return irreducible_polynomials

    def compute_element_orders(self, irr_poly: list) -> dict:
        """Возвращает словарь порядков всех элементов"""

        orders_elements = {}
        n = 0
        for element in self.field[1:]:

            const_x = element.copy()
            counter = 1
            dynamic_poly = self.__mul__(const_x, const_x, irr_poly)

            n += 1
            while dynamic_poly != element:
                dynamic_poly = self.__mul__(dynamic_poly, const_x, irr_poly)
                counter += 1

            orders_elements[tuple(element)] = counter

        return orders_elements

    def __mul__(self, first_poly, second_poly, irr_poly):
        """Операция умножения многочленов путем деления многочлена на неприводимый и взятие остатка"""

        x_mul = symbols('x')
        poly1 = Poly(first_poly, x_mul)
        second_poly = Poly(second_poly, x_mul)

        res = (poly1 * second_poly).all_coeffs()
        new_result = [element % self.p for element in res]
        new_result = Poly(new_result, x_mul)

        irr_poly = Poly(irr_poly, x_mul)

        new_result = div(new_result, irr_poly)[1].all_coeffs()
        new_result = abs((len(first_poly)) - len(new_result)) * [0] + new_result

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

    def __add__(self, poly1: list, poly2: list):
        """Реализует операцию сложения по модулю p"""

        poly1 = np.array(poly1)
        poly2 = np.array(poly2)
        return list((poly1 + poly2) % self.p)

    def __str__(self):
        """Дает возможность вызывать функцию print() на класс"""
        return str(list(map(list, product(self.elements, repeat=self.n))))


if __name__ == '__main__':
    x = symbols('x')
    a, b = int(input("Введите простое число p: ")), int(input("Введите натуральное число n: "))
    gf = GaloisField(a, b)

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
        if order == gf.p ** gf.n - 1:
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

    first_poly_add = abs(gf.n - len(first_poly_add.all_coeffs())) * [0] + first_poly_add.all_coeffs()
    second_poly_add = abs(gf.n - len(second_poly_add.all_coeffs())) * [0] + second_poly_add.all_coeffs()

    if first_poly_add not in gf.field or second_poly_add not in gf.field:
        raise ValueError('Введите многочлены из поля Галуа')

    mul_res_add = gf.__add__(first_poly_add, second_poly_add)
    print(Poly(mul_res_add, x, domain='ZZ').as_expr())
