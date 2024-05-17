import sys
from sha3 import SHA3_256


def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def write_file(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(data)


def main(input_path, output_path):
    # Чтение текста из файла
    input_text = read_file(input_path)
    # Инициализация класса SHA3_256
    sha3 = SHA3_256()
    # Хеширование текста
    hashed_output = sha3.hash(input_text.encode('utf-8'))
    # Запись хеша в файл, конвертация из bytes в hex string
    write_file(output_path, hashed_output.hex())


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: main.py <input_path> <output_path>")
    else:
        input_path = sys.argv[1]
        output_path = sys.argv[2]
        main(input_path, output_path)
