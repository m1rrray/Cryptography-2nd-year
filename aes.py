from constants import S_BOX, INV_S_BOX, R_CON

Nb = 4
Nr = 10
Nk = 4


class AES:
    def __init__(self, key, Nr=10, Nk=4):
        self.key = key
        self.Nr = Nr
        self.Nk = Nk

    def encrypt(self, input_bytes):
        state = [[] for j in range(4)]

        for b in range(4):
            for c in range(4):
                state[b].append(input_bytes[c + 4 * b])

        expended_key = self.__key_expansion()
        state = self.__add_round_key(state, expended_key[:4])
        for i in range(1, self.Nr):
            state = self.__sub_bytes(state)
            state = self.__shift_rows(state)
            state = self.__mix_columns(state)
            state = self.__add_round_key(state, expended_key[i * 4:i * 4 + 4])

        state = self.__sub_bytes(state)
        state = self.__shift_rows(state)
        state = self.__add_round_key(state, expended_key[self.Nr * 4:self.Nr * 4 + 4])

        ans = [None for i in range(16)]

        for b in range(4):
            for c in range(4):
                ans[c + 4 * b] = state[b][c]

        return ans

    def decrypt(self, input_bytes):
        state = [[] for j in range(4)]

        for b in range(4):
            for c in range(4):
                state[b].append(input_bytes[c + 4 * b])

        expended_key = self.__key_expansion()
        state = self.__add_round_key(state, expended_key[self.Nr * 4:self.Nr * 4 + 4])
        for i in range(self.Nr - 1, 0, -1):
            state = self.__shift_rows(state, inv=True)
            state = self.__sub_bytes(state, inv=True)
            state = self.__add_round_key(state, expended_key[i * 4:i * 4 + 4])
            state = self.__mix_columns(state, inv=True)

        state = self.__shift_rows(state, inv=True)
        state = self.__sub_bytes(state, inv=True)
        state = self.__add_round_key(state, expended_key[:4])

        ans = [None for i in range(16)]

        for b in range(4):
            for c in range(4):
                ans[c + 4 * b] = state[b][c]

        return ans

    def __key_expansion(self):
        """Расширение ключа

        Логика:
        У нас есть ключ размером 4*Nk байт, мы его записываем в expanded_keys, деля на 4 столбца.
        Далее, если у нас i индекс столбца кратен 4, то мы берем i - 1 столбец, применяем к нему rot_word,
        потом sub_word, далее делаем xor с i-4 столбцом и R_CON[i//4 - 1].
        Если i не кратен 4, то просто делаем xor i - 1 столбца с i-4 столбцом.

        """
        expanded_keys = [self.key[i:i + 4] for i in range(0, len(self.key), 4)]
        for i in range(4, 4 * (self.Nr + 1)):
            temp = expanded_keys[i - 1]

            if i % 4 == 0:
                temp = list(self.__sub_word(self.__rot_word(temp)))
                temp = [a ^ b for a, b in zip(temp, R_CON[i // self.Nk - 1])]

            expanded_keys.append([a ^ b for a, b in zip(expanded_keys[i - 4], temp)])

        return expanded_keys

    @staticmethod
    def __sub_bytes(state, inv=False):
        """Замена каждого байта в состоянии на соответствующий байт из S-блока"""

        if not inv:
            box = S_BOX
        else:
            box = INV_S_BOX

        for i in range(4):
            for j in range(4):
                state[i][j] = box[state[i][j]]
        return state

    @staticmethod
    def __shift_rows(state, inv=False):
        """Сдвигает строки состояния по количеству байт, определенному номером строки"""
        if not inv:
            state[0][1], state[1][1], state[2][1], state[3][1] = state[1][1], state[2][1], state[3][1], state[0][1]
            state[0][2], state[1][2], state[2][2], state[3][2] = state[2][2], state[3][2], state[0][2], state[1][2]
            state[0][3], state[1][3], state[2][3], state[3][3] = state[3][3], state[0][3], state[1][3], state[2][3]
        else:
            state[0][1], state[1][1], state[2][1], state[3][1] = state[3][1], state[0][1], state[1][1], state[2][1]
            state[0][2], state[1][2], state[2][2], state[3][2] = state[2][2], state[3][2], state[0][2], state[1][2]
            state[0][3], state[1][3], state[2][3], state[3][3] = state[1][3], state[2][3], state[3][3], state[0][3]

        return state

    def __mix_columns(self, state, inv=False):
        """Перемножает столбцы state на фиксированную матрицу"""
        for c in range(4):
            s0 = state[c][0]
            s1 = state[c][1]
            s2 = state[c][2]
            s3 = state[c][3]

            if not inv:
                state[c][0] = self.__multiply_bytes(s0, 0x02) ^ self.__multiply_bytes(s1, 0x03) ^ s2 ^ s3
                state[c][1] = s0 ^ self.__multiply_bytes(s1, 0x02) ^ self.__multiply_bytes(s2, 0x03) ^ s3
                state[c][2] = s0 ^ s1 ^ self.__multiply_bytes(s2, 0x02) ^ self.__multiply_bytes(s3, 0x03)
                state[c][3] = self.__multiply_bytes(s0, 0x03) ^ s1 ^ s2 ^ self.__multiply_bytes(s3, 0x02)
            else:
                state[c][0] = self.__multiply_bytes(s0, 0x0e) ^ self.__multiply_bytes(s1, 0x0b) ^ self.__multiply_bytes(
                    s2, 0x0d) ^ self.__multiply_bytes(s3, 0x09)
                state[c][1] = self.__multiply_bytes(s0, 0x09) ^ self.__multiply_bytes(s1, 0x0e) ^ self.__multiply_bytes(
                    s2, 0x0b) ^ self.__multiply_bytes(s3, 0x0d)
                state[c][2] = self.__multiply_bytes(s0, 0x0d) ^ self.__multiply_bytes(s1, 0x09) ^ self.__multiply_bytes(
                    s2, 0x0e) ^ self.__multiply_bytes(s3, 0x0b)
                state[c][3] = self.__multiply_bytes(s0, 0x0b) ^ self.__multiply_bytes(s1, 0x0d) ^ self.__multiply_bytes(
                    s2, 0x09) ^ self.__multiply_bytes(s3, 0x0e)

        return state

    @staticmethod
    def __add_round_key(state, round_key):
        """Замена столбцов в state с помощью xor с round_key"""
        for i in range(4):
            for j in range(4):
                state[i][j] ^= round_key[i][j]
        return state

    @staticmethod
    def __multiply_by_x(b):
        """Умножение байта на x в поле GF(2^8)"""
        shifted = b << 1
        if shifted & 0x100:
            shifted ^= 0x011b  # x^8 + x^4 + x^3 + x + 1
        return shifted

    def __multiply_bytes(self, a, b):
        """Умножение байтов a и b в поле GF(2^8)"""
        result = 0
        for _ in range(8):
            if b & 1:
                result ^= a
            b >>= 1
            a = self.__multiply_by_x(a)
        return result

    @staticmethod
    def __sub_word(word):
        """Замена байтов слова с использованием S-блока"""
        return (S_BOX[b] for b in word)

    @staticmethod
    def __rot_word(word):
        """Циклический сдвиг слова на один байт влево"""
        return word[1:] + word[:1]


key128 = [0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c]
key192 = [0x8e, 0x80, 0x73, 0x90, 0xb0, 0x79, 0xf7, 0xe5, 0xda, 0x62, 0x0e, 0xf8, 0x64, 0xea, 0x52, 0xd2, 0xc8, 0x52,
          0x10, 0x2c, 0xf3, 0x6b, 0x2b, 0x7b]
key256 = [0x60, 0x3d, 0xeb, 0x10, 0x15, 0xca, 0x71, 0xbe, 0x2b, 0x73, 0xae, 0xf0, 0x85, 0x7d, 0x77, 0x81, 0x1f, 0x35,
          0x2c, 0x07, 0x3b, 0x61, 0x08, 0xd7, 0x2d, 0x98, 0x10, 0xa3, 0x09, 0x14, 0xdf, 0xf4]

byte_text = [
    0x32, 0x43, 0xf6, 0xa8, 0x88, 0x5a, 0x30, 0x8d, 0x31, 0x31, 0x98, 0xa2, 0xe0, 0x37, 0x07, 0x34
]
AesObject = AES(key192, 14, 8)
encrypted = AesObject.encrypt(byte_text)
print([hex(i) for i in encrypted])
decrypted = AesObject.decrypt(encrypted)
print([hex(i) for i in decrypted])
