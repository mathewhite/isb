import json


def load_text(file_path: str) -> str:
    """
    Предназначена для чтения текстового содержимого из файла по указанному пути
    :param file_path: Путь к файлу
    :return: Функция возвращает текст файла
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Файл не найден: {file_path}")
    except Exception as e:
        print(f"Не удалось открыть файл: {e}")


def write_text(data: str, file_path: str) -> None:
    """
    Предназначена для сохранения текстовых данных в файл по указанному пути
    :param file_path: Путь к файлу
    :param data: Текстовые данные, которые нужно записать в файл
    :return: None
    """
    try:
        with open(file_path, "w", encoding="utf8") as file:
            file.write(data)
    except Exception as e:
        print(f"Не удалось записать файл: {e}")


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


def write_json(data: dict, filename: str) -> None:
    """
    Записывает данные в json-файл.
    :param data: словарь с данными для записи
    :param filename: путь к файлу, в который будут записаны данные
    """
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"ошибка при сохранении файла {filename}: {e}")
