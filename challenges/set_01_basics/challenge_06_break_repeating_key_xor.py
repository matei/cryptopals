import base64
import os
from cryptoutils.english_stat import avg_edit_size, find_english_message_by_single_byte_xor
from utils.print_utils import *


class Challenge06:

    def __init__(self):
        """
        Init
        """
        self.path = 'data/challenge06.txt'
        with(open(os.path.join(os.path.dirname(__file__), self.path), 'r')) as f:
            self.data = f.read()

    def display(self):
        """
        Display challenge info
        :return:
        """
        print_line(f'{BOLD_START}Break repeating-key XOR{BOLD_END}', color=BLUE)
        print_line(f'There\'s a file: {self.path}. It\'s been base64ed after being encrypted with repeating-key XOR. ',
                   color=BLUE)
        print_line('Decrypt it.', color=BLUE)

    def run(self):
        """
        So here we need to break repeating key XOR. We'll do that by:
        - calculate key-size by trying various key sizes, for each key size: calculate avg edit size between blocks of that size
        - knowing the key-size, split cipher-text into blocks of that size
        - transpose the blocks
        - solve each block as it were a single char xor (prev challenge strategy)
        :return:
        """
        message_bytes = base64.b64decode(self.data)
        keysize_scores = {avg_edit_size(message_bytes.decode(), keysize, 0, keysize): keysize for keysize in
                          range(2, 40)}
        keysize = keysize_scores[min(keysize_scores.keys())]
        blocks = [message_bytes[i: min(i + keysize, len(message_bytes))] for i in range(0, len(message_bytes), keysize)]
        transposed_blocks = [[b[i] for b in blocks if i < len(b)] for i in range(keysize)]
        key_chars = ''.join(
            [find_english_message_by_single_byte_xor(bytes(block).decode(),
                                                     treat_as_hex_string=False, return_detailed=True)['key'] for block
             in transposed_blocks]
        )
        print(f'Challenge #6 key: {key_chars}')
