import argparse
import sys
import json

from hybrid_crypto_system import CryptoManager
from config import config


def setup_arg_parser():
    """
    Настраивает парсер аргументов командной строки.
    """
    parser = argparse.ArgumentParser(
        description="Гибридная криптосистема Camellia-RSA",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    gen = subparsers.add_parser("gen", help="Генерация ключей")
    gen.add_argument("--sk", default=config["PATH_TO_SYM_KEY"],
                     help="Файл симметричного ключа")
    gen.add_argument("--pub", default=config["PATH_TO_PUBLIC_KEY"],
                     help="Файл публичного ключа RSA")
    gen.add_argument("--priv", default=config["PATH_TO_PRIVATE_KEY"],
                     help="Файл приватного ключа RSA")
    gen.add_argument("--size", type=int, choices=config["CAMELLIA_KEY_SIZES"],
                     default=config["DEFAULT_CAMELLIA_KEY_SIZE"],
                     help="Размер ключа Camellia")

    enc = subparsers.add_parser("enc", help="Шифрование файла")
    enc.add_argument("input", nargs='?', default=config["PATH_TO_INPUT_FILE"],
                     help="Файл для шифрования")
    enc.add_argument("--out", default=config["PATH_TO_ENCRYPTED_FILE"],
                     help="Выходной файл")
    enc.add_argument("--sk", default=config["PATH_TO_SYM_KEY"],
                     help="Файл симметричного ключа")
    enc.add_argument("--priv", default=config["PATH_TO_PRIVATE_KEY"],
                     help="Файл приватного ключа RSA")

    dec = subparsers.add_parser("dec", help="Дешифрование файла")
    dec.add_argument("input", nargs='?', default=config["PATH_TO_ENCRYPTED_FILE"],
                     help="Файл для дешифрования")
    dec.add_argument("--out", default=config["PATH_TO_DECRYPTED_FILE"],
                     help="Выходной файл")
    dec.add_argument("--sk", default=config["PATH_TO_SYM_KEY"],
                     help="Файл симметричного ключа")
    dec.add_argument("--priv", default=config["PATH_TO_PRIVATE_KEY"],
                     help="Файл приватного ключа RSA")

    return parser


def execute_command(args):
    """
    Выполняет выбранную команду.
    """
    try:
        match args.command:
            case "gen":
                CryptoManager.generate_keys(args.sk, args.pub, args.priv, args.size)
            case "enc":
                CryptoManager.encrypt_file(args.input, args.out, args.priv, args.sk)
            case "dec":
                CryptoManager.decrypt_file(args.input, args.out, args.priv, args.sk)
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


def load_json(file_path: str) -> dict:
    """
    Предназначена для чтения json файла
    :param file_path: путь к файлу
    :return: данные json в виде словаря
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Файл не найден: {file_path}")


def main():
    parser = setup_arg_parser()
    args = parser.parse_args()
    execute_command(args)


if __name__ == '__main__':
    main()
