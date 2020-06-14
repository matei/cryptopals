import base64
import os
from cryptoutils.aes import decrypt_aes_128_cbc
from utils.print_utils import *


class Challenge10:

    def __init__(self):
        self.path = 'data/challenge10.txt'
        self.key = 'YELLOW SUBMARINE'
        self.iv = b'0' * 16
        with(open(os.path.join(os.path.dirname(__file__), self.path), 'r')) as f:
            self.data = f.read()

    def display(self):
        print_line(f'{BOLD_START}Implement CBC mode{BOLD_END}', color=BLUE)
        print_line('Implement CBC mode by hand...', color=BLUE)
        print_line(f'The file {self.path} is intelligible (somewhat) when CBC decrypted against "YELLOW SUBMARINE" with an IV of all ASCII 0 (\x00\x00\x00 &c) ')

    def run(self):
        message_bytes = base64.b64decode(self.data)
        print_line(f'Challenge #10 flag: {decrypt_aes_128_cbc(message_bytes, self.key, self.iv).decode("latin-1")}', color=GREEN)