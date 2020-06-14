import base64
import time
from cryptoutils.aes import *
from utils.print_utils import *


class Challenge12:

    def __init__(self):
        self.key = generate_random_aes_key()
        self.input = 'Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg\
                      aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq\
                      dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg\
                      YnkK'.replace('\s', '').replace("\n", '')

    def display(self):
        print_line(f'{BOLD_START}Byte-at-a-time ECB decryption {BOLD_END}', color=BLUE)
        print_line('Implement a new function that encrypts buffers under ECB mode using a consistent but unknown key (for instance, assign a single random key, once, to a global variable).  ', color=BLUE)
        print_line('Now take that same function and have it append to the plaintext, BEFORE ENCRYPTING, the following string: ', color=BLUE)
        print_line(self.input, color=WHITE)
        print_line('Base64 decode the string before appending it. Do not base64 decode the string by hand; make your code do it. The point is that you don\'t know its contents. ', color=BLUE)
        print_line('What you have now is a function that produces: ')
        print_line('AES-128-ECB(your-string || unknown-string, random-key)', color=WHITE)
        print_line('It turns out: you can decrypt "unknown-string" with repeated calls to the oracle function! ', color=BLUE)
        print_line('Here\'s roughly how: ')
        print_line('1. Feed identical bytes of your-string to the function 1 at a time --- start with 1 byte ("A"), then "AA", then "AAA" and so on. Discover the block size of the cipher. You know it, but do this step anyway. ', color=BLUE)
        print_line('2. Detect that the function is using ECB. You already know, but do this step anyways. ', color=BLUE)
        print_line('3. Knowing the block size, craft an input block that is exactly 1 byte short (for instance, if the block size is 8 bytes, make "AAAAAAA"). Think about what the oracle function is going to put in that last byte position. ', color=BLUE)
        print_line('4. Make a dictionary of every possible last byte by feeding different strings to the oracle; for instance, "AAAAAAAA", "AAAAAAAB", "AAAAAAAC", remembering the first block of each invocation. ', color=BLUE)
        print_line('5. Match the output of the one-byte-short input to one of the entries in your dictionary. You\'ve now discovered the first byte of unknown-string. ', color=BLUE)
        print_line('6. Repeat for the next byte. ', color=BLUE)

    def run(self):
        last, keysize = '', 0
        for i in range(32):
            message = 'A' * i
            result = self.oracle(message)
            if i > 2 and last[0:i-1] == result[0:i-1]:
                keysize = i - 1
                print(f'Detected key size {keysize}')
                break
            last = result
        mode = detect_aes_encryption_mode(self.oracle('A' * 120))
        print(f'Detected AES mode: {mode}')
        full_length_encrypted = len(self.oracle('A' * keysize))
        block_count = math.floor(full_length_encrypted / keysize)
        len_l1, len_l2, len_l3 = 0, 0, 0
        precomputed = {}
        print(RED + 'Color for encrypted' + NC)
        print(CYAN + 'Color for injected known padding' + NC)
        print(LGREEN + 'Color for discovered content' + NC)
        for i in range(keysize):
            precomputed[i] = {}
            precomputed[i]['plain'] = b'A' * (keysize - i - 1)
            precomputed[i]['enc'] = self.oracle(precomputed[i]['plain'].decode())
        result = b''
        for b in range(block_count):
            for i in range(keysize):
                for k in range(256):
                    c = k.to_bytes(1, sys.byteorder)
                    enc = self.oracle((precomputed[i]['plain'] + result + c).decode())
                    len_l1, len_l2, len_l3 = render_vis(precomputed[0]['enc'], precomputed[i]['plain'], result, c, b, keysize, len_l1, len_l2, len_l3)
                    time.sleep(0.001)
                    if enc[b * keysize:(b+1)*keysize] == precomputed[i]['enc'][b * keysize:(b+1)*keysize]:
                        result += c
                        break
        print('')
        print('Challenge #12 flag: ' + result.decode())

    def oracle(self, message):
        message_bytes = bytearray(message.encode())
        for b in base64.b64decode(self.input):
            message_bytes.append(b)
        message_bytes = pkcs7_pad(bytes(message_bytes), len(self.key))
        return encrypt_aes_128_ecb(message_bytes, self.key)


def render_vis(enc, plain, known, c, b, keysize, last_length1 = 0, last_length2 = 0, last_length3 = 0):
    """
    Render frame
    :param enc:
    :param plain:
    :param known:
    :param c:
    :param b:
    :param keysize:
    :param last_length1:
    :param last_length2:
    :param last_length3:
    :return:
    """
    up = "\033[A"
    back = "\b"
    if last_length3 > 0 or last_length2 > 0 or last_length1 > 0:
        if last_length3 > 0:
            sys.stdout.write(back * last_length3)
            sys.stdout.write(up)
            sys.stdout.write(back * last_length2)
            sys.stdout.write(up)
            sys.stdout.write(back * last_length1)
        elif last_length2 > 0:
            sys.stdout.write(back * last_length2)
            sys.stdout.write(up)
            sys.stdout.write(back * last_length1)
        else:
            sys.stdout.write(back * last_length1)
    known_space = ' ' if len(known) > 0 else ''
    line1 = display_byte_list(plain, CYAN) + known_space + display_byte_list(known, LGREEN) + RED + ' ' + hex(int.from_bytes(c, sys.byteorder)).replace('0x', '').rjust(3, '0') + NC
    enc_displayed = [' ' for _ in range(keysize-1)] + list(enc)
    len_known = len(known)
    line2 = display_byte_list([be for be in enc_displayed][len_known:len_known + (b+1) * keysize], RED)
    line3 = LGREEN + 'Discovered content: ' + known.decode().replace("\n", " [NL] ") + NC
    sys.stdout.write(line1)
    if len(line2) > 0:
        sys.stdout.write("\n")
        sys.stdout.write(line2)
    if len(line3) > 0:
        sys.stdout.write("\n")
        sys.stdout.write(line3)
    return len(line1), len(line2), len(line3)


def display_byte_list(byte_list, color):
    """
    Display bytes
    :param byte_list:
    :param color:
    :return:
    """
    return color + ' '.join(str(b).rjust(3, '0') for b in byte_list) + NC