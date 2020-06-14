import base64
import binascii
from utils.print_utils import *


class Challenge01:

    def __init__(self):
        self.string = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'
        self.output = 'SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t'

    def display(self):
        print_line(f'{BOLD_START}Convert hex to base64{BOLD_END}', color=BLUE)
        print_line('The string:', color=BLUE)
        print_line(self.string, color=WHITE)
        print_line('shold produce:', color=BLUE)
        print_line(self.output, color=WHITE)

    def run(self):
        print_line('Running challenge #1', color=GREEN)
        result = base64.b64encode(binascii.unhexlify(self.string)).decode()
        print_line(f'Result is {result}')
        print_line(f'Expected result is {self.output}')
        if result == self.output:
            print_line('They match!', color=GREEN)
            print_line(f'Bonus: challenge #1 flag is: {base64.b64decode(result).decode()}', color=GREEN)
        else:
            print_line('They do not match :(', color=RED)
