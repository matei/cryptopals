import binascii
import os
from cryptoutils.english_stat import find_english_message_by_single_byte_xor
from utils.print_utils import *


class Challenge04:

    def __init__(self):
        """
        Init
        """
        print(__file__)
        self.path = 'data/challenge04.txt'
        with(open(os.path.join(os.path.dirname(__file__), self.path), 'r')) as f:
            self.data = f.read()
        self.data = self.data.replace("\n", '')

    def display(self):
        """
        Display challeenge info
        :return:
        """
        print_line(f'{BOLD_START}Detect single-character XOR{BOLD_END}', color=BLUE)
        print_line(f'One of the 60-character strings in {self.path} has been encrypted by single-character XOR.', color=BLUE)
        print_line('Find it. ', color=BLUE)

    def run(self):
        """
        Here we use what we did in challenge 3 on the chunks to see which one yields highest score on english matching
        :return:
        """
        text = self.data
        chunks = [binascii.unhexlify(text[i: min(i + 60, len(text))]).decode('latin-1') for i in range(0, len(text), 60)]
        processed = {r['score']: r['message'].decode() for r in list(map(lambda c: find_english_message_by_single_byte_xor(c, return_detailed=True), chunks))}
        result = processed[max(processed.keys())]
        print_line(f'Challenge #4 flag: {result}', color=GREEN)
