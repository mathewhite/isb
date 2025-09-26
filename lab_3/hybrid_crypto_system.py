from config import config
from file_work import FileWork
from camellia import CamelliaCipher
from rsa import RSA


class HybridCryptoSystem:
    def __init__(self):
        """
        Инициализирует новую гибридную криптосистему.
        """
        self.camellia_key = None
        self.rsa_public_key = None
        self.rsa_private_key = None

    def generate_keys(self, camellia_key_size=config["DEFAULT_CAMELLIA_KEY_SIZE"], rsa_key_size=2048):
        """
        Генерирует новые криптографические ключи для системы.
        :param camellia_key_size: Размер ключа Camellia в битах
        :param rsa_key_size: Размер ключа RSA в битах
        :return: Кортеж из трех элементов (camellia_key, rsa_public_key, rsa_private_key)
        """
        if camellia_key_size not in config["CAMELLIA_KEY_SIZES"]:
            raise ValueError(
                f"Недопустимый размер ключа Camellia ({camellia_key_size} бит). "
                f"Допустимые значения: {config["CAMELLIA_KEY_SIZES"]}"
            )
        self.camellia_key = CamelliaCipher.generate_camellia_key(camellia_key_size)
        self.rsa_private_key, self.rsa_public_key = RSA.generate_rsa_keys(rsa_key_size)
        return self.camellia_key, self.rsa_public_key, self.rsa_private_key

    def save_keys(self, symmetric_key_path=config["PATH_TO_SYM_KEY"],
                  public_key_path=config["PATH_TO_PUBLIC_KEY"],
                  private_key_path=config["PATH_TO_PRIVATE_KEY"]):
        """
        Сохраняет все ключи системы в указанные файлы.
        :param symmetric_key_path: Путь для сохранения зашифрованного ключа Camellia
        :param public_key_path: Путь для сохранения публичного ключа RSA
        :param private_key_path: Путь для сохранения приватного ключа RSA
        :return: Зашифрованный ключ Camellia
        """
        encrypted_cam_key = self.encrypt_camellia_key()
        FileWork.write_file(symmetric_key_path, encrypted_cam_key)
        RSA.save_rsa_keys(self.rsa_private_key, self.rsa_public_key, private_key_path, public_key_path)
        return encrypted_cam_key

    def encrypt_camellia_key(self):
        """
        Шифрует симметричный ключ Camellia с помощью RSA.
        :return: Зашифрованный ключ Camellia
        """
        if not self.camellia_key or not self.rsa_public_key:
            raise ValueError("Ключи не инициализированы")
        return RSA.encrypt_rsa(self.rsa_public_key, self.camellia_key)

    def decrypt_camellia_key(self, encrypted_key):
        """
        Расшифровывает ключ Camellia с помощью RSA.
        :param encrypted_key: Зашифрованный ключ Camellia
        :return: Расшифрованный ключ Camellia
        """
        if not self.rsa_private_key:
            raise ValueError("Приватный ключ RSA не установлен")
        self.camellia_key = RSA.decrypt_rsa(self.rsa_private_key, encrypted_key)
        return self.camellia_key

    def load_keys(self, symmetric_key_path=config["PATH_TO_SYM_KEY"],
                  private_key_path=config["PATH_TO_PRIVATE_KEY"]):
        """
        Загружает ключи из файлов.
        :param symmetric_key_path: Путь к файлу с зашифрованным ключом Camellia
        :param private_key_path: Путь к файлу с приватным ключом RSA
        :return: Расшифрованный ключ Camellia или None при ошибке
        """
        self.rsa_private_key = RSA.load_rsa_private_key(private_key_path)
        encrypted_cam_key = FileWork.read_file(symmetric_key_path)
        if encrypted_cam_key:
            return self.decrypt_camellia_key(encrypted_cam_key)
        return None

    def encrypt_file(self, input_file=config["PATH_TO_INPUT_FILE"],
                     output_file=config["PATH_TO_ENCRYPTED_FILE"]):
        """
        Шифрует файл с помощью Camellia.
        :param input_file: Путь к исходному файлу
        :param output_file: Путь для сохранения зашифрованного файла
        :return: Зашифрованные данные или None при ошибке
        """
        if not self.camellia_key:
            raise ValueError("Ключ Camellia не установлен")

        plaintext = FileWork.read_file(input_file)
        if plaintext is None:
            return None

        cipher = CamelliaCipher(self.camellia_key)
        ciphertext = cipher.encrypt(plaintext)
        FileWork.write_file(output_file, ciphertext)
        return ciphertext

    def decrypt_file(self, input_file=config["PATH_TO_ENCRYPTED_FILE"],
                     output_file=config["PATH_TO_DECRYPTED_FILE"]):
        """
        Расшифровывает файл, зашифрованный Camellia.
        :param input_file: Путь к зашифрованному файлу
        :param output_file: Путь для сохранения расшифрованного файла
        :return: Расшифрованные данные или None при ошибке
        """
        if not self.camellia_key:
            raise ValueError("Ключ Camellia не установлен")

        ciphertext = FileWork.read_file(input_file)
        if ciphertext is None:
            return None

        cipher = CamelliaCipher(self.camellia_key)
        plaintext = cipher.decrypt(ciphertext)
        FileWork.write_file(output_file, plaintext)
        return plaintext


class CryptoManager:
    @staticmethod
    def generate_keys(sym_key_path=config["PATH_TO_SYM_KEY"],
                      pub_key_path=config["PATH_TO_PUBLIC_KEY"],
                      priv_key_path=config["PATH_TO_PRIVATE_KEY"],
                      camellia_key_size=config["DEFAULT_CAMELLIA_KEY_SIZE"]):
        """
        Генерация ключевой пары.
        :param sym_key_path: Путь к файлу симметричного ключа
        :param pub_key_path: Путь к публичному ключу RSA
        :param priv_key_path: Путь к приватному ключу RSA
        :param camellia_key_size: Размер ключа Camellia в битах
        """
        crypto = HybridCryptoSystem()
        crypto.generate_keys(camellia_key_size)
        crypto.save_keys(sym_key_path, pub_key_path, priv_key_path)
        print(f"Ключи сгенерированы (Camellia: {camellia_key_size} бит)")

    @staticmethod
    def encrypt_file(input_path, output_path=config["PATH_TO_ENCRYPTED_FILE"],
                     priv_key_path=config["PATH_TO_PRIVATE_KEY"],
                     sym_key_path=config["PATH_TO_SYM_KEY"]):
        """
        Шифрование файла.
        :param input_path: Путь к исходному файлу
        :param output_path: Путь для зашифрованного файла
        :param priv_key_path: Путь к приватному ключу RSA
        :param sym_key_path: Путь к симметричному ключу
        :return: Статус операции (True/False)
        """
        if not FileWork.file_exists(input_path):
            print(f"Файл не найден: {input_path}")
            return False

        crypto = HybridCryptoSystem()
        if not crypto.load_keys(sym_key_path, priv_key_path):
            print("Ошибка загрузки ключей")
            return False

        if crypto.encrypt_file(input_path, output_path):
            print(f"Файл зашифрован: {input_path} → {output_path}")
            return True
        return False

    @staticmethod
    def decrypt_file(input_path, output_path=config["PATH_TO_DECRYPTED_FILE"],
                     priv_key_path=config["PATH_TO_PRIVATE_KEY"],
                     sym_key_path=config["PATH_TO_SYM_KEY"]):
        """
        Дешифрование файла.
        :param input_path: Путь к зашифрованному файлу
        :param output_path: Путь для расшифрованного файла
        :param priv_key_path: Путь к приватному ключу RSA
        :param sym_key_path: Путь к симметричному ключу
        :return: Статус операции (True/False)
        """
        if not FileWork.file_exists(input_path):
            print(f"Файл не найден: {input_path}")
            return False

        crypto = HybridCryptoSystem()
        if not crypto.load_keys(sym_key_path, priv_key_path):
            print("Ошибка загрузки ключей")
            return False

        if crypto.decrypt_file(input_path, output_path):
            print(f"Файл расшифрован: {input_path} → {output_path}")
            return True
        return False
