from cryptoutils.aes import has_valid_pkcs7_pad, strip_pkcs7_pad
from utils.print_utils import *


class Challenge15:

    def __init__(self):
        """
        Init
        """
        self.test1 = 'ICE ICE BABY\x04\x04\x04\x04'
        self.test2 = 'ICE ICE BABY\x05\x05\x05\x05'
        self.test3 = 'ICE ICE BABY\x01\x02\x03\x04'

    def display(self):
        """
        Display challenge info
        :return:
        """
        print_line(f'{BOLD_START}PKCS#7 padding validation{BOLD_END}', color=BLUE)
        print_line('Write a function that takes a plaintext, determines if it has valid PKCS#7 padding, and strips the padding off.')
        print_line('The string:', color=BLUE)
        print_line(self.test1)
        print_line('has valid padding, and produces the result "ICE ICE BABY".', color=BLUE)
        print_line('The string:', color=BLUE)
        print_line(self.test2)
        print_line('does not have valid padding, nor does:')
        print_line(self.test3)

    def run(self):
        """
        Write function that validates pkcs7 padding by standard def
        :return:
        """
        for string in [self.test1, self.test2, self.test3]:
            if print_has_valid_padding(string.encode()):
                print_line(f'Stripped: {strip_pkcs7_pad(string.encode())}', color=GREEN)


def print_has_valid_padding(string):
    has = has_valid_pkcs7_pad(string)
    print_line(f'{string.decode()} has valid padding', color=GREEN) if has else print_line(f'{string} does not have valid padding', color=GREEN)
    return has