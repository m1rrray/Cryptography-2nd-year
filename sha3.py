class SHA3_256:
    # Определение констант, используемых в алгоритме
    BYTE_SIZE = 8  # Размер байта в битах
    INT_SIZE = 64  # Размер целого числа в битах
    ROUND_COUNT = 24  # Количество раундов
    BYTE_1 = 0x80  # Константа для дополнения
    BIT_LENGTH = 1600  # Общая длина битов в состоянии Keccak
    HASH_LENGTH = 256  # Длина хеша в битах
    RATE = BIT_LENGTH - 2 * HASH_LENGTH  # Скорость, используемая в конструкции губки
    # Константы раунда для функции iota
    RC = [0x0000000000000001, 0x0000000000008082, 0x800000000000808A,
          0x8000000080008000, 0x000000000000808B, 0x0000000080000001,
          0x8000000080008081, 0x8000000000008009, 0x000000000000008A,
          0x0000000000000088, 0x0000000080008009, 0x000000008000000A,
          0x000000008000808B, 0x800000000000008B, 0x8000000000008089,
          0x8000000000008003, 0x8000000000008002, 0x8000000000000080,
          0x000000000000800A, 0x800000008000000A, 0x8000000080008081,
          0x8000000000008080, 0x0000000080000001, 0x8000000080008008]

    def __init__(self):
        # Инициализация состояния Keccak нулями
        self.state = bytearray([0] * (self.BIT_LENGTH // self.BYTE_SIZE))

    def _rotate_left(self, a, n):
        # Циклический сдвиг влево
        return ((a >> (self.INT_SIZE - (n % self.INT_SIZE))) + (a << (n % self.INT_SIZE))) % (1 << self.INT_SIZE)

    def _theta(self, A):
        # Функция θ (theta): XOR каждого бита с некоторыми битами его столбца
        C = [A[x][0] ^ A[x][1] ^ A[x][2] ^ A[x][3] ^ A[x][4] for x in range(5)]
        D = [C[(x - 1) % 5] ^ self._rotate_left(C[(x + 1) % 5], 1) for x in range(5)]
        return [[A[x][y] ^ D[x] for y in range(5)] for x in range(5)]

    def _rho(self, A):
        # Функция ρ (rho): циклические сдвиги битов внутри каждой линии
        rotations = [
            [0, 36, 3, 41, 18],
            [1, 44, 10, 45, 2],
            [62, 6, 43, 15, 61],
            [28, 55, 25, 21, 56],
            [27, 20, 39, 8, 14]
        ]
        return [[self._rotate_left(A[x][y], rotations[x][y]) for y in range(5)] for x in range(5)]

    def _pi(self, A):
        # Функция π (pi): перестановка позиций битов
        return [[A[(x + 3 * y) % 5][x] for y in range(5)] for x in range(5)]

    def _chi(self, A):
        # Функция χ (chi): нелинейное преобразование битов
        return [[A[x][y] ^ ((~A[(x + 1) % 5][y]) & A[(x + 2) % 5][y]) for y in range(5)] for x in range(5)]

    def _iota(self, A, round_idx):
        # Функция ι (iota): добавление раундовой константы
        A[0][0] ^= self.RC[round_idx]
        return A

    def _keccak_f(self):
        # Основная функция перестановки Keccak
        lanes = [
            [self._load(self.state[self.BYTE_SIZE * (x + 5 * y):self.BYTE_SIZE * (x + 5 * y) + self.BYTE_SIZE]) for y in
             range(5)] for x in range(5)]
        for round_idx in range(self.ROUND_COUNT):
            lanes = self._theta(lanes)
            lanes = self._rho(lanes)
            lanes = self._pi(lanes)
            lanes = self._chi(lanes)
            lanes = self._iota(lanes, round_idx)
        for x in range(5):
            for y in range(5):
                self.state[self.BYTE_SIZE * (x + 5 * y):self.BYTE_SIZE * (x + 5 * y) + self.BYTE_SIZE] = self._store(
                    lanes[x][y])

    def _load(self, b):
        # Загрузка битов из массива байтов в целочисленное значение
        return sum((b[i] << (self.BYTE_SIZE * i)) for i in range(self.BYTE_SIZE))

    def _store(self, a):
        # Сохранение целочисленного значения обратно в массив байтов
        return bytearray((a >> (self.BYTE_SIZE * i)) % 256 for i in range(self.BYTE_SIZE))

    def hash(self, input_data):
        # Основная функция хеширования
        rate_in_bytes = self.RATE // self.BYTE_SIZE
        input_bytes = bytearray(input_data)
        input_offset = 0

        while input_offset < len(input_bytes):
            block_size = min(len(input_bytes) - input_offset, rate_in_bytes)
            for i in range(block_size):
                self.state[i] ^= input_bytes[i + input_offset]
            input_offset += block_size
            if block_size == rate_in_bytes:
                self._keccak_f()

        # Добавление дополнения к последнему блоку
        self.state[block_size] ^= 0x06
        if block_size == (rate_in_bytes - 1):
            self._keccak_f()
        self.state[rate_in_bytes - 1] ^= self.BYTE_1
        self._keccak_f()

        # Получение итогового значения хеша
        output_bytes = bytearray()
        while len(output_bytes) < (self.HASH_LENGTH // self.BYTE_SIZE):
            output_bytes += self.state[:rate_in_bytes]
            self._keccak_f()

        return output_bytes[:self.HASH_LENGTH // self.BYTE_SIZE]


# Usage example
# sha3 = SHA3_256()
# input_data = bytes("aboba", 'utf-8')
# hash_output = sha3.hash(input_data)
# print("SHA3-256 Hash:", hash_output.hex())
