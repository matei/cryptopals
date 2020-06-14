import base64
import os
from cryptoutils.aes import decrypt_aes_128_ecb
from utils.print_utils import *


class Challenge07:

    def __init__(self):
        """
        Init
        """
        self.path = 'data/challenge07.txt'
        with(open(os.path.join(os.path.dirname(__file__), self.path), 'r')) as f:
            self.data = f.read()
        self.key = 'YELLOW SUBMARINE'

    def display(self):
        """
        Display challenge info
        :return:
        """
        print_line(f'{BOLD_START}AES in ECB mode{BOLD_END}', color=BLUE)
        print_line(f'The Base64-encoded content in {self.path} has been encrypted via AES-128 in ECB mode under the key')
        print_line(self.key, color=WHITE)
        print_line('(case-sensitive, without the quotes; exactly 16 characters; I like "YELLOW SUBMARINE" because it\'s exactly 16 bytes long, and now you do too). ', color=BLUE)
        print_line('Decrypt it. You know the key, after all. ', color=BLUE)

    def run(self):
        """
        Simple AES ECB decryption
        :return:
        """
        message_bytes = base64.b64decode(self.data)
        print('Challenge #7 flag:')
        print(decrypt_aes_128_ecb(message_bytes, self.key).decode())