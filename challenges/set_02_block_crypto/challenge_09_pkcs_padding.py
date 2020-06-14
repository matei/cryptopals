from cryptoutils.aes import pkcs7_pad
from utils.print_utils import *


class Challenge09:

    def __init__(self):
        self.string = 'YELLOW SUBMARINE'
        self.expected = b'YELLOW SUBMARINE\x04\x04\x04\x04'

    def display(self):
        print_line(f'{BOLD_START}Implement PKCS#7 padding{BOLD_END}', color=BLUE)
        print_line('A block cipher transforms a fixed-sized block (usually 8 or 16 bytes) of plaintext into ciphertext. But we almost never want to transform a single block; we encrypt irregularly-sized messages. ', color=BLUE)
        print_line('One way we account for irregularly-sized messages is by padding, creating a plaintext that is an even multiple of the blocksize. The most popular padding scheme is called PKCS#7. ', color=BLUE)
        print_line('So: pad any block to a specific block length, by appending the number of bytes of padding to the end of the block. For instance, ', color=BLUE)
        print_line(self.string)
        print_line('... padded to 20 bytes would be: ')
        print_line(self.expected)

    def run(self):
        message = "YELLOW SUBMARINE"
        length = 20
        result = pkcs7_pad(message.encode(), length)
        if result == self.expected:
            print_line(f'Challenge #9 flag: {result}', color=GREEN)
        else:
            print_line(f'Unexpected result {result}')
