from sympy import symbols, Poly
from main import GaloisField

alphabet = "abcdefghijklmnopqrstuvwxyz "


def encoder(alpha, beta, text):
    gf = GaloisField(3, 3)
    shifr_text = []
    blocks_text = {w: z for w, z in zip(alphabet, gf.field)}

    for block in blocks_text.values():
        new_alpha = gf.__mul__(alpha, block, (1, 0, 2, 2))
        new_block = gf.__add__(new_alpha, beta)
        shifr_text.append(new_block)

    shifered_symbols = {t: q for t, q in zip(alphabet, shifr_text)}

    ans = []
    for symbol in text:
        galois_symbol = shifered_symbols[symbol]
        encode_symbol = alphabet[list(blocks_text.values()).index(galois_symbol)]
        ans.append(encode_symbol)

    ans = ''.join(ans)
    return ans


def decoder(alpha, beta, shifr_text):
    gf = GaloisField(3, 3)

    alphabet_galois = {w: z for w, z in zip(alphabet, gf.field)}
    minus_beta = [(-i) % gf.p for i in beta]

    reversed_alpha = []
    for element in gf.field:
        product = gf.__mul__(element, alpha, (1, 0, 2, 2))
        if product == [0, 0, 1]:
            reversed_alpha = element

    ans = []
    for symbol in shifr_text:
        summa = gf.__add__(alphabet_galois[symbol], minus_beta)
        galois_symbol = gf.__mul__(summa, reversed_alpha, (1, 0, 2, 2))
        decode_symbol = alphabet[list(alphabet_galois.values()).index(galois_symbol)]
        ans.append(decode_symbol)

    ans = ''.join(ans)
    return ans



x = symbols('x')
print(f'Такой алфавит вы используетет: {alphabet}')
alpha_interface = Poly(input('Введите alpha из мультипликативной группы Галуа F(3)^3 : '), x, domain='ZZ')
beta_interface = Poly(input('Введите beta из поля Галуа: '), x, domain='ZZ')

alpha_interface = abs(3 - len(alpha_interface.all_coeffs())) * [0] + alpha_interface.all_coeffs()
beta_interface = abs(3 - len(beta_interface.all_coeffs())) * [0] + beta_interface.all_coeffs()
text_interface = input('Введите текст, который хотите зашифровать: ')
a = encoder(alpha_interface, beta_interface, text_interface)
print(f'Зашифрованный текст: {a}')
shifr_text_interface = input('Введите текст, который хотите расшифровать: ')
b = decoder(alpha_interface, beta_interface, shifr_text_interface)
print(f'Расшифрованный текст: {b}')


