from helper import *


def caesar_cipher(decrypted: str, key: int, alphabet: str) -> str:
    """
        Предназначена зашифровки текста по заданному значению сдвига
        :param alphabet: алфавит с которым работает шифр
        :param decrypted: Начальный текст
        :param key: значение сдвига
        :return: зашифрованный текст
    """
    encrypted = ""
    length = len(alphabet)
    for char in decrypted:
        if char == '\n':
            encrypted += char
            continue
        elif char not in alphabet:
            encrypted += char
            continue
        encrypted += alphabet[(alphabet.find(char) + key) % length]
    return encrypted


def caesar_decipher(encrypted: str, key: int, alphabet: str) -> str:
    """
        Предназначена зашифровки текста по заданному значению сдвига
        :param alphabet: алфавит с которым работает шифр
        :param encrypted: Начальный текст
        :param key: значение сдвига
        :return: расшифрованный текст
    """
    decrypted = ""
    length = len(alphabet)
    for char in encrypted:
        if char == '\n':
            decrypted += char
            continue
        elif char not in alphabet:
            decrypted += char
            continue
        decrypted += alphabet[(alphabet.find(char) - key) % length]
    return decrypted


def main():
    settings = load_json("config.json")
    decrypted = load_text(settings["decrypted_text_file"]).upper()
    alphabet = settings["alphabet"]
    way_to_save = settings["encrypted_text_file"]
    shift = settings["shift"]
    encrypted = caesar_cipher(decrypted, shift, alphabet)
    write_text(encrypted, way_to_save)


if __name__ == "__main__":
    main()
