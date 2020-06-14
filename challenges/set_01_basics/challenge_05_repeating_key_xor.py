import binascii
from cryptoutils.common import xor_bytes_repeating_key
from utils.print_utils import *


class Challenge05:

    def __init__(self):
        self.input1 = "Burning 'em, if you ain't quick and nimble\n"
        self.input2 = 'I go crazy when I hear a cymbal'
        self.expected1 = '0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272'
        self.expected2 = 'a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f'
        self.key = 'ICE'

    def display(self):
        print_line(f'{BOLD_START}Implement repeating-key XOR{BOLD_END}', color=BLUE)
        print_line('Here is the opening stanza of an important work of the English language: ', color=BLUE)
        print_line(self.input1, color=WHITE)
        print_line(self.input2, color=WHITE)
        print_line('Encrypt it, under the key "ICE", using repeating-key XOR. ', color=BLUE)
        print_line('In repeating-key XOR, you\'ll sequentially apply each byte of the key; the first byte of plaintext will be XORed against I, the next C, the next E, then I again for the 4th byte, and so on', color=BLUE)
        print_line('It should come out to: ', color=BLUE)
        print_line(self.expected1, color=WHITE)
        print_line(self.expected2, color=WHITE)

    def run(self):
        result = xor_bytes_repeating_key(
            (self.input1 + self.input2).encode(),
            self.key.encode()
        )
        if binascii.hexlify(result).decode() == self.expected1 + self.expected2:
            print_line(f'Got expected result!', color=GREEN)
        else:
            print_line(f'Challenge #5 failed.', color=RED)

