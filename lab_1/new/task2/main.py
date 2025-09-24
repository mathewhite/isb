from helper import *


def get_frequency(text: str) -> dict:
    """
    Вычисляет частоту встречаемости каждого символа в тексте.
    :param text: входной текст
    :return: словарь, ключи - символы, значения - их частоты
    """
    if not text:
        raise ZeroDivisionError("файл пуст")
    freq_dict = {}
    for char in text:
        if char.lower() in freq_dict:
            freq_dict[char.lower()] += 1
        else:
            freq_dict[char.lower()] = 1

    for char, count in freq_dict.items():
        freq_dict[char] = count / len(text)
    return dict(sorted(freq_dict.items(), key=lambda item: item[1], reverse=True))


def decrypt(text: str, key: dict) -> str:
    """
    Заменяет символы в тексте согласно переданному ключу.
    :param text: исходный текст
    :param key: словарь замен
    :return: новый текст, в котором символы заменены в соответствии с ключом
    """
    decrypted = ""
    for char in text:
        print(char)
        decrypted_char = key.get(char)
        if decrypted_char is None:
            decrypted_char = char
        decrypted += decrypted_char
    return decrypted


def main():
    settings = load_json("config.json")
    encrypted_text = load_text(settings["encrypted_text_file"])
    frequency = get_frequency(encrypted_text)
    write_json(frequency, settings["char_frequency_file"])
    key = load_json(settings["key"])
    decrypted_text = decrypt(encrypted_text, key)
    write_text(decrypted_text, settings["decrypted_text_file"])


if __name__ == "__main__":
    main()
