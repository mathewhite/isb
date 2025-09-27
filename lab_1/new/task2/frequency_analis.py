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