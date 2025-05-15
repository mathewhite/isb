import json


def get_initial_text(path: str) -> str:
    """
        Получает текст из файла.

        Args:
            path (str): Путь к файлу с текстом.

        Returns:
            str: Текст для шифрования.
        """
    try:
        with open(path, mode  ='r', encoding='utf-8') as file:
            return file.read().upper()
    except (FileNotFoundError, UnicodeDecodeError) as e:
        raise ValueError(f"Ошибка при чтении файла {path}: {e}")


def encrypting(initial_text: str, alphabet: str, key: int, output_path: str):
    """
        Шифрует текст с использованием шифра Цезаря.

        Args:
            initial_text (str): Исходный текст для шифрования.
            alphabet (str): Алфавит, используемый для шифрования.
            key (int): Ключ для сдвига символов.
            output_path (str): Путь для сохранения зашифрованного текста.
        """
    if not alphabet:
        raise ValueError("Алфавит не может быть пустым.")
    if not isinstance(key, int):
        raise ValueError("Ключ должен быть целым числом.")

    dct = {alphabet[i]: alphabet[(i + key) % len(alphabet)] for i in range(len(alphabet))}
    text_list=list(initial_text)
    for i in range(len(text_list)):
        if text_list[i] in dct:
            text_list[i] = dct[text_list[i]]
    encrypted_text = ''.join(text_list)

    try:
        with open(output_path, mode="w", encoding="utf-8") as file:
            file.write(encrypted_text)
    except IOError as e:
        raise ValueError(f"Ошибка при записи в файл {output_path}: {e}")


def main():
    """
        Основная функция программы.
    """
    with open('settings.json', mode='r', encoding='utf-8') as file:
        settings = json.load(file)
    text = get_initial_text(settings['initial_text'])
    key = settings['key']
    alphabet = settings['alphabet']
    output_path = settings['output_path']
    encrypting(text, alphabet, key, output_path)


if __name__ == "__main__":
    main()






