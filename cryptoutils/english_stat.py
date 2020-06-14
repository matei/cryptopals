import binascii
import math
import string
from .common import xor_bytes_repeating_key


def score_against_english(message):
    """
    Calculate a score of english resemblance for message.
    Calculates by comparing top 6 most frequent characters in message resemblance with english top 6
    and top 6 least frequent with english top 6 least frequent

    :param message: string
    :return:
    """

    # frequency taken from http://en.wikipedia.org/wiki/Letter_frequency
    english_letter_freq = {'A': 8.17, 'B': 1.29, 'C': 2.78, 'D': 4.25, 'E': 12.7, 'F': 2.23, 'G': 2.02, 'H': 6.09, 'I': 6.97, 'J': 0.15, 'K': 0.77, 'L': 4.03, 'M': 2.41, 'N': 6.75, 'O': 7.51, 'P': 1.93, 'Q': 0.1, 'R': 5.99, 'S': 6.33, 'T': 9.06, 'U': 2.76, 'V': 0.98, 'W': 2.36, 'X': 0.15, 'Y': 1.97, 'Z': 0.07}
    english = dict_frequency_string(english_letter_freq)
    frequency_message = dict_frequency_string(letter_frequency(message))
    score = 0
    # rank each of the first 6 in english are also first 6 in message
    for c in english[:6]:
        if c in frequency_message[:6]:
            score += 1
    # rank each of last 6 in english are also last 6 in message
    for c in english[-6:]:
        if c in frequency_message[-6:]:
            score += 1
    return score


def find_english_message_by_single_byte_xor(message, treat_as_hex_string=False, return_detailed=False):
    """
    Decodes single-byte--key-xor-encrypted string with all readable characters
    and returns the one best resembling english using score_against_english() function

    :param return_detailed:
    :param message: string - can be either bytes string or raw string
    :param treat_as_hex_string: whether bytes string was passed and needs decoding or not
    :return: best guess decoded string and corresponding byte used as key
    """
    bytes_string = binascii.unhexlify(message) if treat_as_hex_string else message.encode()
    result = {}
    for c in string.printable:
        try:
            xored = xor_bytes_repeating_key(bytes_string, c.encode('latin-1'))
            score = score_against_english(xored.decode())
            result[score] = {'message': xored, 'key': c, 'score': score}
        except UnicodeDecodeError:
            pass
    return result[max(result.keys())] if return_detailed else result[max(result.keys())]['message'].decode()


def edit_size(s1, s2):
    """
    Calculate Hamming (edit) distance between 2 strings - which is actually number of different bits
    :param s1: string
    :param s2: string
    :return: int
    """
    return abs(len(s1) - len(s2)) * 8 + sum([bin(ord(s1[i]) ^ ord(s2[i])).count('1') for i in range(min([len(s1), len(s2)]))])


def avg_edit_size(message, block_size, block_count=2, normalization_factor=1):
    """
    Calculate avg edit size between sequential blocks in message
    :param message:
    :param block_size:
    :param block_count:
    :param normalization_factor:
    :return:
    """
    block_count = math.floor(len(message) / block_size) if block_count == 0 else block_count
    chunks = [message[i:min(i+block_size, len(message))] for i in range(0, len(message), block_size)][0:block_count]
    score = 0
    if len(chunks) < 2:
        return score
    for i in range(len(chunks) - 1):
        score += edit_size(chunks[i], chunks[i+1]) / normalization_factor
    return score / (len(chunks) - 1)


def dict_frequency_string(frequency_dict):
    """
    Transforms dictionary into string composed from keys sorted by values. Used to score against english
    :param frequency_dict: dict
    :return: string
    """
    return ''.join([k for k, v in sorted(frequency_dict.items(), key=lambda item: item[1], reverse=True)])


def letter_frequency(string_to_parse):
    """
    Returns dictionary with characters / frequency in string_to_parse
    :param string_to_parse: string
    :return: dict
    """
    return {chr(char): string_to_parse.upper().count(chr(char)) for char in range(ord('A'), ord('Z') + 1)}
