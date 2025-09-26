import json


def load_config():
    """Загружает конфигурацию из JSON файла"""
    try:
        with open('const.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Ошибка: Файл const.json не найден")
        raise


config = load_config()
