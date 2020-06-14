import string
import random
from cryptoutils.aes import generate_random_aes_key, encrypt_aes_128_ecb, encrypt_aes_128_cbc, pkcs7_pad, detect_aes_encryption_mode
from utils.print_utils import *


class Challenge11:

    def __init__(self):
        """
        Init
        """
        self.key = generate_random_aes_key()
        self.iv = b'0' * len(self.key)

    def display(self):
        """
        Display challenge info
        :return:
        """
        print_line(f'{BOLD_START}An ECB/CBC detection oracle{BOLD_END}', color=BLUE)
        print_line('Now that you have ECB and CBC working: ', color=BLUE)
        print_line('Write a function to generate a random AES key; that\'s just 16 random bytes. ', color=BLUE)
        print_line('Write a function that encrypts data under an unknown key --- that is, a function that generates a random key and encrypts under it. ', color=BLUE)
        print_line('Under the hood, have the function append 5-10 bytes (count chosen randomly) before the plaintext and 5-10 bytes after the plaintext. ', color=BLUE)
        print_line('Now, have the function choose to encrypt under ECB 1/2 the time, and under CBC the other half (just use random IVs each time for CBC). Use rand(2) to decide which to use. ', color=BLUE)
        print_line('Detect the block cipher mode the function is using each time. You should end up with a piece of code that, pointed at a block box that might be encrypting ECB or CBC, tells you which one is happening. ', color=BLUE)

    def run(self):
        """
        Re-use has_repeating_chunks strategy to detect ECB.
        Since we control the input, it's just a matter of choosing a long enough message
        :return:
        """
        message = 'A' * 12000
        textlen = len(message)
        block_size = 120
        blocks = [message[i:min(i + block_size, textlen)] for i in range(0, textlen, block_size)][0:100]
        correctness = 0
        tries = 0
        guessed_ecb_correct = 0
        guessed_cbc_correct = 0
        guessed_ecb_total = 0
        guessed_cbc_total = 0
        encrypted_times_ecb = 0
        encrypted_times_cbc = 0
        for block in blocks:
            encrypted, mode = self.encrypt_message_with_random_key(block)
            detected_mode = detect_aes_encryption_mode(encrypted)
            tries += 1
            if mode == 'CBC':
                encrypted_times_cbc += 1
            else:
                encrypted_times_ecb += 1
            if detected_mode == 'CBC':
                guessed_cbc_total += 1
            else:
                guessed_ecb_total += 1
            if mode == detected_mode:
                correctness += 1
                if detected_mode == 'CBC':
                    guessed_cbc_correct += 1
                else:
                    guessed_ecb_correct += 1
            print_line(f'Detected {detected_mode} encryption mode. Encrypted with {mode}', color=GREEN)
        print_line(f'Correctness ratio: {100 * (round(correctness / tries, 2))}% in {tries} blocks', color=GREEN)
        print_line(f'Detected {guessed_ecb_total} times ECB. Nailed it {guessed_ecb_correct} times. Total times used was {encrypted_times_ecb}', color=GREEN)
        print_line(f'Detected {guessed_cbc_total} times CBC. Nailed it {guessed_cbc_correct} times. Total times used was {encrypted_times_cbc}', color=GREEN)

    def encrypt_message_with_random_key(self, message):
        """
        Encrypt message with random prefix and suffix
        :param message:
        :return:
        """
        alphabet = list(string.ascii_letters + string.digits)
        random.shuffle(alphabet)
        message = f'{"".join(alphabet[0:random.randrange(5, 10)])}{message}'
        random.shuffle(alphabet)
        message += ''.join(alphabet[:random.randrange(5, 10)])
        random.shuffle(alphabet)
        encryption_mode = random.randrange(2)
        if encryption_mode == 1:
            # CBC
            return encrypt_aes_128_cbc(pkcs7_pad(message.encode(), 16), self.key, self.iv), 'CBC'
        else:
            # ECB
            return encrypt_aes_128_ecb(pkcs7_pad(message.encode(), 16), self.key), 'ECB'