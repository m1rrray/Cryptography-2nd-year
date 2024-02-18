import argparse
from aes import AES


def encrypt_file(input_file, output_file, key):
    with open(input_file, 'r') as f:
        plaintext = f.read()

    key = key.split('0x')
    key.pop(0)
    key = [int(i, base=16) for i in key]

    if len(key) not in (16, 24, 32):
        raise ValueError("Invalid key length. Must be 128, 192, or 256 bits")

    aes = AES(key=key)

    byte_text = plaintext.split("0x")
    byte_text.pop(0)
    byte_text = [int(i, base=16) for i in byte_text]

    ciphertext = aes.encrypt(byte_text)

    ciphertext = ''.join([hex(i) for i in ciphertext])
    with open(output_file, 'w') as f:
        f.write(ciphertext)


def decrypt_file(input_file, output_file, key):
    with open(input_file, 'r') as f:
        ciphertext = f.read()

    key = key.split('0x')
    key.pop(0)
    key = [int(i, base=16) for i in key]

    if len(key) not in (16, 24, 32):
        raise ValueError("Invalid key length. Must be 128, 192, or 256 bits")

    aes = AES(key=key)

    byte_text = ciphertext.split("0x")
    byte_text.pop(0)
    byte_text = [int(i, base=16) for i in byte_text]

    open_text = aes.decrypt(byte_text)

    open_text = ''.join([hex(i) for i in open_text])
    with open(output_file, 'w') as f:
        f.write(open_text)


def main():
    parser = argparse.ArgumentParser(description='AES Encryption/Decryption CLI')
    parser.add_argument('input_file', help='Input file path')
    parser.add_argument('output_file', help='Output file path')
    parser.add_argument('key', help='AES key (16 bytes)', type=str)
    parser.add_argument('--decrypt', action='store_true', help='Decrypt the input file')

    args = parser.parse_args()

    if args.decrypt:
        decrypt_file(args.input_file, args.output_file, args.key)
        print("Decryption completed.")
    else:
        encrypt_file(args.input_file, args.output_file, args.key)
        print("Encryption completed.")


if __name__ == "__main__":
    main()
