def xor_bytes_equal_length(byte_array1, byte_array2):
    """
    xor 2 byte arrays
    :param byte_array1:
    :param byte_array2:
    :return:
    """
    assert len(byte_array1) == len(byte_array2)
    return bytes([a ^ b for a, b in zip(byte_array1, byte_array2)])


def xor_bytes_repeating_key(message, key):
    """
    xor bytes array with repeating key
    :param message: bytes
    :param key: bytes
    :return: bytes
    """
    repeating_key = [key[i % len(key)] for i in range(len(message))]
    return bytes([m ^ c for m, c in zip(message, repeating_key)])


def has_repeating_chunks(block, tolerance=1, size=16):
    chunk_times = {}
    chunks = [block[i: min(i+size, len(block))] for i in range(0, len(block), size)]
    for chunk in chunks:
        chunk_times[chunk] = chunk_times.get(chunk, 0) + 1
        if chunk_times[chunk] > tolerance:
            return True
    return False
