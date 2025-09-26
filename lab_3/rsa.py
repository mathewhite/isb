from config import config
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
from file_work import FileWork


class RSA:
    @staticmethod
    def generate_rsa_keys(key_size=2048):
        """
        Генерация пары RSA ключей
        :param key_size: размер ключа в битах
        :return: кортеж (приватный ключ, публичный ключ)
        """
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        return private_key, public_key

    @staticmethod
    def save_rsa_keys(private_key, public_key,
                      priv_path=config["PATH_TO_PRIVATE_KEY"],
                      pub_path=config["PATH_TO_PUBLIC_KEY"]):
        """
        Сохранение RSA ключей в файлы
        :param private_key: закрытый ключ RSA
        :param public_key: открытый ключ RSA
        :param priv_path: путь для сохранения закрытого ключа
        :param pub_path: путь для сохранения открытого ключа
        :return: кортеж (сериализованный закрытый ключ, сериализованный открытый ключ)
        """
        priv_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )

        pub_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        FileWork.write_file(priv_path, priv_pem)
        FileWork.write_file(pub_path, pub_pem)

        return priv_pem, pub_pem

    @staticmethod
    def load_rsa_public_key(pub_path=config["PATH_TO_PUBLIC_KEY"]):
        """
        Загрузка открытого ключа RSA из файла
        :param pub_path: путь к файлу с открытым ключом
        :return: объект открытого ключа или None при ошибке
        """
        pub_pem = FileWork.read_file(pub_path)
        if not pub_pem:
            return None
        return serialization.load_pem_public_key(pub_pem, backend=default_backend())

    @staticmethod
    def load_rsa_private_key(priv_path=config["PATH_TO_PRIVATE_KEY"]):
        """
        Загрузка закрытого ключа RSA из файла
        :param priv_path: путь к файлу с закрытым ключом
        :return: объект закрытого ключа или None при ошибке
        """
        priv_pem = FileWork.read_file(priv_path)
        if not priv_pem:
            return None
        return serialization.load_pem_private_key(priv_pem, password=None, backend=default_backend())

    @staticmethod
    def encrypt_rsa(public_key, plaintext):
        """
        Шифрование данных с помощью RSA-OAEP
        :param public_key: открытый ключ RSA
        :param plaintext: данные для шифрования
        :return: зашифрованные данные
        """
        return public_key.encrypt(
            plaintext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    @staticmethod
    def decrypt_rsa(private_key, ciphertext):
        """
           Дешифрование данных с помощью RSA-OAEP
           :param private_key: закрытый ключ RSA
           :param ciphertext: зашифрованные данные
           :return: расшифрованные данные
           """
        return private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
