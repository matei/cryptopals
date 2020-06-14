from cryptoutils.english_stat import find_english_message_by_single_byte_xor
from utils.print_utils import *


class Challenge03:

    def __init__(self):
        self.message = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'

    def display(self):
        print_line(f'{BOLD_START}Single-byte XOR cipher{BOLD_END}', color=BLUE)
        print_line('The hex encoded string: ', color=BLUE)
        print_line(self.message, color=WHITE)
        print_line('... has been XORed against a single character. Find the key, decrypt the message. ', color=BLUE)
        print_line('How? Devise some method for "scoring" a piece of English plaintext. '
                   'Character frequency is a good metric. '
                   'Evaluate each output and choose the one with the best score.', color=BLUE)

    def run(self):
        print_line(f'Challenge #3 flag is {find_english_message_by_single_byte_xor(self.message, treat_as_hex_string=True, return_detailed=False)}', color=GREEN)
