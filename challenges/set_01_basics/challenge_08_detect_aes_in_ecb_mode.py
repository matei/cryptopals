import binascii
import os
from cryptoutils.common import has_repeating_chunks
from utils.print_utils import *


class Challenge08:

    def __init__(self):
        self.path = 'data/challenge08.txt'
        with(open(os.path.join(os.path.dirname(__file__), self.path), 'r')) as f:
            self.data = f.read()

    def display(self):
        print_line(f'{BOLD_START}Detect AES in ECB mode{BOLD_END}', color=BLUE)
        print_line(f'In {self.path} are a bunch of hex-encoded ciphertexts. ', color=BLUE)
        print_line('One of them has been encrypted with ECB. ', color=BLUE)
        print_line('Detect it. ', color=BLUE)
        print_line('Remember that the problem with ECB is that it is stateless and deterministic; '
                   'the same 16 byte plaintext block will always produce the same 16 byte ciphertext. ', color=BLUE)

    def run(self):
        lines = self.data.split("\n")
        blocks = [binascii.unhexlify(l) for l in lines]
        result = []
        for block in blocks:
            if has_repeating_chunks(block):
                result.append(block)
        print_line('Challenge #8 repeating blocks: {}'.format("\n".join([binascii.hexlify(r).decode() for r in result])), color=GREEN)
