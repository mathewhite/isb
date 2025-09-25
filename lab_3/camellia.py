import const

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os


class CamelliaCipher:
    def __init__(self, key):
        """
        Инициализация шифра Camellia
        :param key: ключ шифрования
        """
        key_length = len(key) * 8
        if key_length not in const.CAMELLIA_KEY_SIZES:
            raise ValueError(
                f"Недопустимая длина ключа Camellia ({key_length} бит). "
                f"Допустимые значения: {const.CAMELLIA_KEY_SIZES}"
            )
        self.key = key

    def encrypt(self, plaintext):
        """
        Шифрование данных
        :param plaintext: открытый текст для шифрования
        :return: зашифрованные данные в формате IV + ciphertext
        """

        iv = os.urandom(const.IV_SIZE)

        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext) + padder.finalize()

        cipher = Cipher(
            algorithms.Camellia(self.key),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        return iv + ciphertext

    def decrypt(self, ciphertext):
        """
        Дешифрование данных
        :param ciphertext: зашифрованные данные в формате IV + ciphertext
        :return: расшифрованный текст
        """
        iv = ciphertext[:const.IV_SIZE]
        actual_ciphertext = ciphertext[const.IV_SIZE:]

        cipher = Cipher(
            algorithms.Camellia(self.key),
            modes.CBC(iv),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(actual_ciphertext) + decryptor.finalize()

        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

        return plaintext

    @staticmethod
    def generate_camellia_key(key_size):
        """
        Генерация случайного ключа для Camellia
        :param key_size: размер ключа в битах
        :return: сгенерированный ключ
        """
        if key_size not in const.CAMELLIA_KEY_SIZES:
            raise ValueError(
                f"Недопустимый размер ключа ({key_size} бит). "
                f"Допустимые значения: {const.CAMELLIA_KEY_SIZES}"
            )
        return os.urandom(key_size // 8)
