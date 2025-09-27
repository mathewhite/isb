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