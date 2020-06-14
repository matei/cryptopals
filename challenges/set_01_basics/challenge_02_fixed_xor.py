import binascii
from cryptoutils.common import xor_bytes_equal_length
from utils.print_utils import *


class Challenge02:

    def __init__(self):
        """
        Init
        """
        self.string = '1c0111001f010100061a024b53535009181c'
        self.xorkey = '686974207468652062756c6c277320657965'
        self.output = '746865206b696420646f6e277420706c6179'

    def display(self):
        """
        Display challenge info
        :return:
        """
        print_line(f'{BOLD_START}Fixed XOR{BOLD_END}', color=BLUE)
        print_line('Write a function that takes two equal-length buffers and produces their XOR combination.', color=BLUE)
        print_line('If your function works properly, then when you feed it the string:')
        print_line(self.string, color=WHITE)
        print_line('... after hex decoding, and when XORed against:', color=BLUE)
        print_line(self.xorkey, color=WHITE)
        print_line('... should produce: ', color=BLUE)
        print_line(self.output, color=WHITE)

    def run(self):
        """
        Simple xoring of equal length
        :return:
        """
        result = xor_bytes_equal_length(
            binascii.unhexlify(self.string),
            binascii.unhexlify(self.xorkey)
        )
        result_string = binascii.hexlify(result).decode()
        print_line(f'XOR result is {result_string}')
        if result_string == self.output:
            print_line('They match!', color=GREEN)
            print_line(f'Bonus: Challenge #2 flag: {binascii.unhexlify(result_string).decode()}', color=GREEN)
        else:
            print_line('Not matching :(', color=RED)
