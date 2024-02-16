from constants import S_BOX, INV_S_BOX, R_CON
import numpy as np

Nb = 4  # number of coloumn of State (for AES = 4)
Nr = 10  # number of rounds ib ciper cycle (if nb = 4 nr = 10)
Nk = 4  # the key length (in 32-bit words)

class AES:
    def __init__(self, key, Nr, Nk):
        self.key = key
        self.Nr = Nr
        self.Nk = Nk



    def
def multiply_by_x(b):
    """Умножение байта на x в поле GF(2^8)"""
    # Сдвигаем на один бит влево
    shifted = b << 1
    # Проверяем является ли старший бит равным 1
    if shifted & 0x100:
        # Если да, то выполняем операцию XOR c неприводимым полиномом
        shifted ^= 0x011b  # x^8 + x^4 + x^3 + x + 1
    return shifted


def multiply_bytes(a, b):
    """Умножение байтов a и b в поле GF(2^8)"""
    result = 0
    for _ in range(8):
        # Если младший бит b равен 1, то выполняем операцию XOR
        if b & 1:
            result ^= a
        # Сдвигаем b на один бит вправо
        b >>= 1
        # Умножаем a на x
        a = multiply_by_x(a)
    return result


def find_inverse(b):
    """Находим обратный элемент для b"""
    for i in range(256):
        if multiply_bytes(b, i) == 1:
            return i


def mix_columns(state):
    """Перемножает столбцы state на фиксированную матрицу"""
    for c in range(4):
        s0 = state[c][0]
        s1 = state[c][1]
        s2 = state[c][2]
        s3 = state[c][3]

        state[c][0] = multiply_bytes(s0, 0x02) ^ multiply_bytes(s1, 0x03) ^ s2 ^ s3
        state[c][1] = s0 ^ multiply_bytes(s1, 0x02) ^ multiply_bytes(s2, 0x03) ^ s3
        state[c][2] = s0 ^ s1 ^ multiply_bytes(s2, 0x02) ^ multiply_bytes(s3, 0x03)
        state[c][3] = multiply_bytes(s0, 0x03) ^ s1 ^ s2 ^ multiply_bytes(s3, 0x02)

    return state


def add_round_key(state, round_key):
    """Замена столбцов в state с помощью xor с round_key"""
    for i in range(4):
        for j in range(4):
            state[i][j] ^= round_key[i][j]
    return state


def sub_bytes(state):
    """Замена каждого байта в состоянии на соответствующий байт из S-блока"""
    for i in range(4):
        for j in range(4):
            state[i][j] = S_BOX[state[i][j]]
    return state


def shift_rows(state):
    """Сдвигает строки состояния по количеству байт, определенному номером строки"""
    state[0][1], state[1][1], state[2][1], state[3][1] = state[1][1], state[2][1], state[3][1], state[0][1]
    state[0][2], state[1][2], state[2][2], state[3][2] = state[2][2], state[3][2], state[0][2], state[1][2]
    state[0][3], state[1][3], state[2][3], state[3][3] = state[3][3], state[0][3], state[1][3], state[2][3]

    return state


def sub_word(word):
    """Замена байтов слова с использованием S-блока"""
    return (S_BOX[b] for b in word)


def rot_word(word):
    """Циклический сдвиг слова на один байт влево"""
    return word[1:] + word[:1]


def key_expansion(key):
    """Расширение ключа

    Логика:
    У нас есть ключ размером 4*Nk байт, мы его записываем в expanded_keys, деля на 4 столбца.
    Далее, если у нас i индекс столбца кратен 4, то мы берем i - 1 столбец, применяем к нему rot_word,
    потом sub_word, далее делаем xor с i-4 столбцом и R_CON[i//4 - 1].
    Если i не кратен 4, то просто делаем xor i - 1 столбца с i-4 столбцом.

    """
    expanded_keys = [key[i:i + 4] for i in range(0, len(key), 4)]
    for i in range(4, 4 * (Nr + 1)):
        temp = expanded_keys[i - 1]

        if i % 4 == 0:
            temp = list(sub_word(rot_word(temp)))
            temp = [a ^ b for a, b in zip(temp, R_CON[i // Nk - 1])]

        expanded_keys.append([a ^ b for a, b in zip(expanded_keys[i - 4], temp)])

    return expanded_keys


def encrypt(input, masterkey):
    state = [[] for j in range(4)]
    for b in range(4):
        for c in range(Nb):
            state[b].append(input[c + 4 * b])
    expended_key = key_expansion(masterkey)
    state = add_round_key(state, expended_key[:4])
    for i in range(1, Nr):
        state = sub_bytes(state)
        state = shift_rows(state)
        state = mix_columns(state)
        state = add_round_key(state, expended_key[i*4:i*4+4])

    state = sub_bytes(state)
    state = shift_rows(state)
    state = add_round_key(state, expended_key[Nr*4:Nr*4+4])

    ans = [None for i in range(4*Nb)]

    for b in range(4):
        for c in range(Nb):
            ans[c + 4 * b] = state[b][c]

    return [hex(i) for i in ans]


key1 = [0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c]
byte_text = [
    0x32, 0x43, 0xf6, 0xa8, 0x88, 0x5a, 0x30, 0x8d, 0x31, 0x31, 0x98, 0xa2, 0xe0, 0x37, 0x07, 0x34
]

print(encrypt(byte_text, key1))