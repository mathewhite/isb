import os


class FileWork:
    @staticmethod
    def read_file(file_path):
        """
        Чтение файла
        :param file_path: путь к файлу
        :return: содержимое файла или None при ошибке
        """
        try:
            with open(file_path, 'rb') as f:
                return f.read()
        except Exception as e:
            print(f"Ошибка чтения файла {file_path}: {str(e)}")
            return None

    @staticmethod
    def write_file(file_path, data):
        """
        Запись данных в файл
        :param file_path: путь к файлу
        :param data: данные для записи
        :return: True при успешной записи, False при ошибке
        """
        try:
            dir_path = os.path.dirname(file_path)
            if dir_path and not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True)

            with open(file_path, 'wb') as f:
                f.write(data)
            print(f"Файл успешно записан: {file_path}")
            return True
        except Exception as e:
            print(f"Ошибка записи файла {file_path}: {str(e)}")
            return False

    @staticmethod
    def file_exists(file_path):
        """
        Проверка существования файла
        :param file_path: путь к файлу
        :return: True если файл существует, иначе False
        """
        return os.path.exists(file_path)
