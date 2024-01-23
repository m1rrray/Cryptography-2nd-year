from sympy import symbols, Poly

from main import GaloisField

alphabet = "abcdefghijklmnopqrstuvwxyz "


# y_i=αx_i+β, i=¯(1,l).

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
    text = []

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

# if __name__ == '__main__':
x = symbols('x')
print(f'Такой алфавит вы используетет: {alphabet}')
alpha = Poly(input('Введите alpha : '), x, domain='ZZ')
beta = Poly(input('Введите beta : '), x, domain='ZZ')

alpha = abs(3 - len(alpha.all_coeffs())) * [0] + alpha.all_coeffs()
beta = abs(3 - len(beta.all_coeffs())) * [0] + beta.all_coeffs()
print(alpha, beta)
a = encoder(alpha, beta, 'aloxa privet')
print(a)
b = decoder(alpha, beta, a)
print(b)
