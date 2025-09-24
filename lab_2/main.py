from helper import *
import math
import scipy.special as sp

def frequency_bit_test(sequence: str) -> float:
    """
    частотный побитовый тест
    :param sequence: битовая последовательность
    :return: Р-значение
    """
    stat = 1 / math.sqrt(len(sequence)) * (sequence.count("1") - sequence.count("0"))
    p_value = math.erfc(stat / math.sqrt(2))
    return p_value


def identical_consecutive_bit_test(sequence: str) -> float:
    """
    тест на одинаковые подряд идущие биты
    :param sequence: битовая последовательность
    :return: Р-значение
    """
    n = len(sequence)
    percent_of_units = sequence.count("1") / n
    if abs(percent_of_units - 0.5) >= (2 / math.sqrt(n)):
        return 0
    switch_counter = 0
    for i in range(n - 1):
        if sequence[i] != sequence[i + 1]:
            switch_counter += 1
    p_value = math.erfc(abs(switch_counter - 2 * n * percent_of_units * (1 - percent_of_units)) / (
            2 * math.sqrt(2 * n) * percent_of_units * (1 - percent_of_units)))
    return p_value


def longest_sequence_in_block(sequence: str, p: list) -> float:
    """
    тест на самую длинную последовательность единиц в блоке
    :param sequence: битовая последовательность
    :param p: теоретические вероятности
    :return: З-значение
    """
    blocks = []
    for i in range(0, len(sequence), 8):
        block = sequence[i: i + 8]
        blocks.append(block)
    v = [0, 0, 0, 0]
    for block in blocks:
        max_run = 0
        cur_len = 0
        for j in block:
            if j == "1":
                cur_len += 1
                max_run = max(max_run, cur_len)
            else:
                cur_len = 0
        match max_run:
            case 0 | 1:
                v[0] += 1
            case 2:
                v[1] += 1
            case 3:
                v[2] += 1
            case _ if max_run >= 4:
                v[3] += 1
    chi2 = sum(((v[i] - 16 * p[i]) ** 2) / (16 * p[i]) for i in range(len(v)))
    p_value = sp.gammainc((3 / 2), (chi2 / 2))
    return p_value

def main():
    settings = load_json("config.json")
    cpp_seq = load_text(settings["cpp_sequence"])
    java_seq = load_text(settings["java_sequence"])
    results = {
        "cpp": {
            "frequency_bit_test": frequency_bit_test(cpp_seq),
            "identical_consecutive_bit_test": identical_consecutive_bit_test(cpp_seq),
            "longest_sequence_in_block": longest_sequence_in_block(cpp_seq, settings["P"])
        },
        "java": {
            "frequency_bit_test": frequency_bit_test(java_seq),
            "identical_consecutive_bit_test": identical_consecutive_bit_test(java_seq),
            "longest_sequence_in_block": longest_sequence_in_block(java_seq, settings["P"])
        }
    }

    write_json(results, settings["results"])


if __name__ == "__main__":
    main()