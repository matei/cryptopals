import functools
import math
import random
import string
import sys
from Crypto.Cipher import AES
from cryptoutils.common import xor_bytes_equal_length, has_repeating_chunks


def decrypt_aes_128_ecb(message_bytes, key):
    """
    Decrypt AES ECB
    :param message_bytes:
    :param key:
    :return:
    """
    decipher = AES.new(key, AES.MODE_ECB)
    return decipher.decrypt(message_bytes)


def encrypt_aes_128_ecb(message_bytes, key):
    """
    Encrypt AES ECB
    :param message_bytes:
    :param key:
    :return:
    """
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(message_bytes)


def pkcs7_pad(message, length):
    message_len = len(message)
    padding_len = (1 + math.floor(message_len / length)) * length - message_len
    padding = padding_len.to_bytes(1, sys.byteorder)
    for _ in range(padding_len):
        message += padding
    return message


def has_valid_pkcs7_pad(message):
    """
    Check if message has valid pkcs7 padding
    :param message:
    :return:
    """
    len_message = len(message)
    for i in range(len_message):
        from_last = len_message - i - 1
        byte_value = (i + 1).to_bytes(1, sys.byteorder)
        if message[from_last].to_bytes(1, sys.byteorder) == byte_value:
            for j in range(from_last, len_message):
                if message[j].to_bytes(1, sys.byteorder) != byte_value:
                    return False
            # if we made it here, it means all were equal to expected value...
            return True
    # if we made it here, no valid byte found...
    return False


def strip_pkcs7_pad(message):
    if has_valid_pkcs7_pad(message):
        return message[:-1 * message[len(message) - 1]]
    else:
        raise Exception('Bad padding')


def encrypt_aes_128_cbc(message, key, iv):
    """
    Encrypt AES in CBC Mode
    :param message:
    :param key:
    :param iv:
    :return:
    """
    message_length = len(message)
    length = len(key)
    blocks = [message[i:min(i+length, message_length)] for i in range(0, message_length, length)]
    if len(blocks[len(blocks) - 1]) < length:
        blocks[len(blocks) - 1] = pkcs7_pad(blocks[len(blocks) - 1], length)
    encrypted_blocks = []
    last_block = iv
    for block in blocks:
        encrypted_block = encrypt_aes_128_ecb(xor_bytes_equal_length(last_block, block), key)
        encrypted_blocks.append(encrypted_block)
        last_block = encrypted_block
    return functools.reduce(lambda a, b: bytes(a) + bytes(b), encrypted_blocks)


def decrypt_aes_128_cbc(message, key, iv):
    """
    Decrypt AES in CBC mode
    :param message:
    :param key:
    :param iv:
    :return:
    """
    message_length = len(message)
    length = len(key)
    blocks = [message[i:min(i+length, message_length)] for i in range(0, message_length, length)]
    blocks.reverse()
    decrypted_blocks = []

    for i in range(len(blocks)):
        decrypted_block = decrypt_aes_128_ecb(blocks[i], key)
        next_block = blocks[i+1] if i < len(blocks) - 1 else iv
        decrypted_blocks.append(xor_bytes_equal_length(decrypted_block, next_block))
    decrypted_blocks.reverse()
    return functools.reduce(lambda a, b: bytes(a) + bytes(b), decrypted_blocks)


def generate_random_aes_key(length=16):
    """
    Generate random key
    :param length:
    :return:
    """
    ab = list(string.ascii_letters + string.digits)
    random.shuffle(ab)
    return ''.join(ab[:length])


def detect_aes_encryption_mode(message):
    if has_repeating_chunks(message):
        return 'ECB'
    else:
        return 'CBC'
