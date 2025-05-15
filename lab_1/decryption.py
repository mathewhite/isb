import json


def calculate_frequence(text: str) -> dict:
    """
    Вычисляет частоту символов в тексте.
    :param text: Входной текст.
    :return: Словарь соответствия символов их частоте в тексте.
    """
    if not text:
        raise ValueError("Input text can't be empty.")

    symbol_counts = dict()

    for symbol in text:

        if symbol=='\n':
            continue

        if symbol in symbol_counts:
            symbol_counts[symbol] += 1

        else:
            symbol_counts[symbol] = 1

    symbols_count = sum(symbol_counts.values())

    symbol_frequence = dict()

    for char, count in symbol_counts.items():

        frequence = round(count / symbols_count, 6)

        symbol_frequence[char] = frequence

    sorted_frequence_list = sorted(symbol_frequence.items(), key=lambda item: item[1], reverse=True)

    sorted_freq = dict(sorted_frequence_list)

    return sorted_freq

def create_mapping(encrypt_frequence: dict, rus_frequence: dict) -> dict:
    """
    Сопоставляет символы зашифрованного текста с русскими символами по частоте.
    :param encrypt_frequence: Словарь частот символов из зашифрованного текста.
    :param rus_frequence: Словарь ожидаемых частот русских символов.
    :return: Словарь соответствия зашифрованных символов русским символам.
    """
    if not encrypt_frequence or not rus_frequence:
        raise ValueError("Input dictionaries cannot be empty.")

    encrypt_rus_dict = {}

    encrypt_frequence_list = list(encrypt_frequence.items())
    rus_frequence_list = list(rus_frequence.items())

    for i in range(min(len(rus_frequence), len(encrypt_frequence))):

        encrypt_rus_dict[encrypt_frequence_list[i][0]] = rus_frequence_list[i][0]

    return encrypt_rus_dict


def decrypt_text(encrypted_text: str, key: dict) -> str:
    """
    Расшифровывает текст с использованием соответствия символов.
    :param encrypted_text: Зашифрованный текст.
    :param key: Словарь соответствия зашифрованных символов расшифрованным.
    :return: Расшифрованный текст.
    """
    if not encrypted_text:
        raise ValueError("Encrypted text can't be empty.")

    if not key:
        raise ValueError("Dictionary cannot be empty.")

    decrypted_text = []

    for symbol in encrypted_text:
        if symbol in key:
            decrypted_text.append(key[symbol])
        else:
            decrypted_text.append(symbol)

    return ''.join(decrypted_text)


def main():
    with open('settings-2.json', mode="r", encoding='utf-8') as file:
        settings= json.load(file)

    russian_statistics= settings['russian_statistics']
    with open(settings['initial_text'], mode="r", encoding='utf-8') as file:
        initial_text = file.read()
    output_path= settings['output_path']
    key_path= settings['key_path']
    decrypted_statistics= calculate_frequence(initial_text)
    key= create_mapping(decrypted_statistics, russian_statistics)
    text= decrypt_text(initial_text, key)
    with open(output_path, mode="w", encoding='utf-8') as file:
        file.write(text)


if __name__ == "__main__":
    main()
