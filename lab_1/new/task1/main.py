import argparse

from helper import *
from caesar import *


def parse_arguments():
    """Парсит аргументы из командной строки"""
    defaults = load_json("config.json")

    parser = argparse.ArgumentParser(description='Шифр Цезаря - шифрование и дешифрование текста')

    parser.add_argument('--mode',
                        choices=['encrypt', 'decrypt'],
                        default='encrypt',
                        help='Режим работы: encrypt (шифрование) или decrypt (дешифрование)')

    parser.add_argument('--input-file',
                        type=str,
                        default=defaults['decrypted_text_file'],
                        help='Путь к входному файлу с текстом')

    parser.add_argument('--output-file',
                        type=str,
                        default=defaults['encrypted_text_file'],
                        help='Путь к выходному файлу для результата')

    parser.add_argument('--shift',
                        type=int,
                        default=defaults['shift'],
                        help='Величина сдвига для шифра Цезаря')

    parser.add_argument('--alphabet',
                        type=str,
                        default=defaults['alphabet'],
                        help='Алфавит для шифрования')

    return parser.parse_args()


def main():
    args = parse_arguments()

    text = load_text(args.input_file).upper()

    if args.mode == 'encrypt':
        result = caesar_cipher(text, args.shift, args.alphabet)
        write_text(result, args.output_file)
        print(f"Текст зашифрован и сохранен в {args.output_file}")
    else:
        result = caesar_decipher(text, args.shift, args.alphabet)
        write_text(result, args.output_file)
        print(f"Текст расшифрован и сохранен в {args.output_file}")


if __name__ == "__main__":
    main()
