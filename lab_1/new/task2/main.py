import argparse

from helper import *
from frequency_analis import *
from decrypter import *


def parse_arguments():
    """Парсит аргументы из командной строки"""
    defaults = load_json("config.json")

    parser = argparse.ArgumentParser(description='Анализ частот и дешифрование текста')

    parser.add_argument('--encrypted-file',
                        type=str,
                        default=defaults['encrypted_text_file'],
                        help='Путь к файлу с зашифрованным текстом')

    parser.add_argument('--decrypted-file',
                        type=str,
                        default=defaults['decrypted_text_file'],
                        help='Путь к файлу для сохранения расшифрованного текста')

    parser.add_argument('--frequency-file',
                        type=str,
                        default=defaults['char_frequency_file'],
                        help='Путь к файлу для сохранения частотного анализа')

    parser.add_argument('--key-file',
                        type=str,
                        default=defaults['key'],
                        help='Путь к файлу с ключом для дешифрования')

    return parser.parse_args()


def main():
    args = parse_arguments()
    encrypted_text = load_text(args.encrypted_file)
    frequency = get_frequency(encrypted_text)
    write_json(frequency, args.frequency_file)
    print(f"Частотный анализ сохранен в {args.frequency_file}")

    key = load_json(args.key_file)
    decrypted_text = decrypt(encrypted_text, key)

    write_text(decrypted_text, args.decrypted_file)
    print(f"Расшифрованный текст сохранен в {args.decrypted_file}")


if __name__ == "__main__":
    main()
