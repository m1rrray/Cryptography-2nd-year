import argparse
from rsa import RSA


def main():
    parser = argparse.ArgumentParser(description='Программа шифрования RSA с работой через файлы.')
    subparsers = parser.add_subparsers(dest='command', help='доступные команды')

    # Подкоманда для генерации ключевой пары
    parser_keypair = subparsers.add_parser('genkey', help='генерация ключевой пары')
    parser_keypair.add_argument('--p', type=int, required=True, help='простое число p')
    parser_keypair.add_argument('--q', type=int, required=True, help='простое число q')

    # Подкоманда для шифрования текста
    parser_encrypt = subparsers.add_parser('encrypt', help='шифрование текста')
    parser_encrypt.add_argument('--input', type=str, required=True, help='путь к файлу с открытым текстом')
    parser_encrypt.add_argument('--e', type=int, required=True, help='часть открытого ключа e')
    parser_encrypt.add_argument('--n', type=int, required=True, help='часть открытого ключа n')
    parser_encrypt.add_argument('--output', type=str, help='путь к файлу для сохранения шифртекста')

    # Подкоманда для дешифрования текста
    parser_decrypt = subparsers.add_parser('decrypt', help='дешифрование текста')
    parser_decrypt.add_argument('--input', type=str, required=True, help='путь к файлу с шифртекстом')
    parser_decrypt.add_argument('--d', type=int, required=True, help='часть закрытого ключа d')
    parser_decrypt.add_argument('--n', type=int, required=True, help='часть закрытого ключа n')
    parser_decrypt.add_argument('--output', type=str, help='путь к файлу для сохранения расшифрованного текста')

    args = parser.parse_args()

    if args.command == 'genkey':
        rsa = RSA(args.p, args.q)
        print("Открытый ключ:", rsa.public_key)
        print("Закрытый ключ:", rsa.private_key)
    elif args.command in ['encrypt', 'decrypt']:
        if args.command == 'encrypt':
            with open(args.input, 'r', encoding='utf-8') as f:
                plaintext = f.read()
            rsa = RSA()
            rsa.public_key = (args.e, args.n)
            ciphertext = rsa.encrypt(plaintext)
            result = ''.join(map(str, ciphertext))
        else:
            with open(args.input, 'r', encoding='utf-8') as f:
                ciphertext = list(map(int, f.read().split()))
            rsa = RSA()
            rsa.private_key = (args.d, args.n)
            result = rsa.decrypt(ciphertext)

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"Результат сохранен в файле {args.output}")



if __name__ == "__main__":
    main()
