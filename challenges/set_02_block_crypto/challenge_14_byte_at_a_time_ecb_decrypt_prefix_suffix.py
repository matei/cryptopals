from cryptoutils.aes import *
from utils.print_utils import *


class Challenge14:

    def __init__(self):
        """
        Init
        """
        self.key = generate_random_aes_key()
        self.keysize = len(self.key)
        self.prefix = 'P1P2P3P4P4P6P7P8P9P10'.encode()
        self.target = 'T1T2T3T4T4T6T7T8T9T10'.encode()

    def display(self):
        """
        Display message
        :return:
        """
        print_line(f'{BOLD_START}Byte-at-a-time ECB decryption (Harder){BOLD_END}', color=BLUE)
        print_line('Take your oracle function from #12. Now generate a random count of random bytes and prepend this string to every plaintext. You are now doing:', color=BLUE)
        print_line('AES-128-ECB(random-prefix || attacker-controlled || target-bytes, random-key)', color=WHITE)
        print_line('Same goal: decrypt the target-bytes. ', color=BLUE)

    def run(self):
        """
        So it goes like this:
        - calculate prefix size and suffix size
        - fill prefix until it fills blocks entirely (it's length % 16 is 0)
        - then re-use strategy from challenge 12 by completely disregarding that prefix is there...
        :return:
        """
        # first calculate prefix size and hwo much padding we need for it
        len_prefix = self.compute_prefix_size()
        padding_length = (len_prefix//self.keysize + 1) * self.keysize - len_prefix
        pad_prefix = b'B' * padding_length
        prefix_block_count = len_prefix//self.keysize + 1 if padding_length % 16 != 0 else len_prefix//self.keysize

        # calculate suffix aka target length.. we need this just to figure out when to stop
        suffix_padding_length = self.compute_suffix_padding_size()
        len_target = len(self.oracle(b'')) - len_prefix - suffix_padding_length
        print_line(f'len target is {len_target}', color=CYAN)

        # generate precomputed dict as in challenge 12
        precomputed = self.generate_precomputed_dict(pad_prefix)

        # now perform the brute-force similar to challenge 12
        block_start = prefix_block_count
        block_count = math.floor(len(self.oracle(b'A' * self.keysize)) / self.keysize)
        result = b''
        for b in range(block_start, block_count):
            for i in range(self.keysize):
                for k in range(0, 256):
                    c = k.to_bytes(1, sys.byteorder)
                    enc = self.oracle(pad_prefix + precomputed[i]['plain'] + result + c)
                    if enc[b * self.keysize:(b+1)*self.keysize] == precomputed[i]['enc'][b*self.keysize:(b+1) * self.keysize]:
                        if len(result) < len_target:
                            result += c
                        break
        if result.decode() == self.target.decode():
            print_line(f'Found! {result.decode()}', color=GREEN)
        elif len(result):
            print_line('Found another result', color=RED)
            print_line(result, color=RED)
            print_line(self.target, color=RED)
        else:
            print_line('No result found', color=RED)

    def generate_precomputed_dict(self, pad_prefix):
        """
        Generate dict with precomputed encrypted messages for all sizes
        :param pad_prefix:
        :return:
        """
        precomputed = {}
        for i in range(self.keysize):
            precomputed[i] = {}
            precomputed[i]['plain'] = b'A' * (self.keysize - i - 1)
            precomputed[i]['enc'] = self.oracle(pad_prefix + precomputed[i]['plain'])
        return precomputed

    def compute_prefix_size(self):
        """
        Calculate the size of the prefix by filling userdata with at least 3 blocks of known identical content
        and find first identical blocks - blocks before those will belong to prefix.
        Then calculate length of prefix in last non-filled block by filling it one by one until it no longer changes
        from previous fills (meaning we no longer have content from suffix in that block)
        :return:
        """
        enc = self.oracle(b'A' * self.keysize * 4)
        prefix_block_count = 0
        for b in range(math.floor(len(enc) / self.keysize)):
            if enc[b * self.keysize: self.keysize * (b + 1)] == enc[self.keysize * (b + 1): self.keysize * (b + 2)]:
                prefix_block_count = b
                break
        print_line(f'Prefix block count: {prefix_block_count}', color=CYAN)
        last_filled_block = b''
        padding_length = 0
        for i in range(self.keysize):
            enc = self.oracle(b'A' * i)
            if enc[self.keysize * (prefix_block_count - 1): self.keysize * prefix_block_count] == last_filled_block:
                padding_length = i - 1
                break
            last_filled_block = enc[self.keysize * (prefix_block_count - 1): self.keysize * prefix_block_count]
        print_line(f'Found padding length is {padding_length}', color=CYAN)
        len_prefix = prefix_block_count * self.keysize - padding_length
        return len_prefix

    def compute_suffix_padding_size(self):
        """
        Calculate suffix padding size by filling up userdata until one more block is added
        :return:
        """
        suffix_padding_length = 0
        last_len = 0
        for i in range(self.keysize):
            enc = self.oracle(b'A' * i)
            if last_len == 0:
                last_len = len(enc)
            else:
                if last_len != len(enc):
                    suffix_padding_length = i
                    break
                last_len = len(enc)
        print_line(f'Suffix padding length = {suffix_padding_length}', color=CYAN)
        return suffix_padding_length

    def oracle(self, message):
        """
        The oracle function
        :param message:
        :return:
        """
        message_bytes = bytearray(self.prefix + message + self.target)
        message_bytes = pkcs7_pad(bytes(message_bytes), len(self.key))
        return encrypt_aes_128_ecb(message_bytes, self.key)
