from cryptoutils.aes import *
from utils.print_utils import *


class Challenge16:

    def __init__(self):
        """
        Init
        """
        self.key = generate_random_aes_key()
        self.keysize = len(self.key)
        self.iv = b'0' * len(self.key)
        self.prefix = 'comment1=cooking%20MCs;userdata='
        self.suffix = ';comment2=%20like%20a%20pound%20of%20bacon'

    def display(self):
        """
        Display challenge info
        :return:
        """
        print_line(f'{BOLD_START}CBC bitflipping attacks{BOLD_END}', color=BLUE)
        print_line('Generate a random AES key. ', color=BLUE)
        print_line('Combine your padding code and CBC code to write two functions. ', color=BLUE)
        print_line('The first function should take an arbitrary input string, prepend the string: ')
        print_line(self.prefix, color=WHITE)
        print_line('.. and append the string:', color=BLUE)
        print_line(self.suffix, color=WHITE)
        print_line('The function should quote out the ";" and "=" characters.', color=BLUE)
        print_line('The function should then pad out the input to the 16-byte AES block length and encrypt it under the random AES key.', color=BLUE)
        print_line('The second function should decrypt the string and look for the characters ";admin=true;"', color=BLUE)
        print_line('If you\'ve written the first function properly, it should not be possible to provide user input to it that will generate the string the second function is looking for', color=BLUE)
        print_line('Instead, modify the ciphertext (without knowledge of the AES key) to accomplish this. ', color=BLUE)

    def run(self):
        """
        The idea is we are filling the prefix up to full block size as usual
        Then we inject a dummy block with known content and then our admin true payload, but we replace the metacharacters = and ; with X and Y
        Then in the cipher-text, we xor the bytes at block index where = and ; would be with X ^ ; and Y ^ = so that when it's xored back during
        decryption, we'll get back our desired payload
        """
        # first calculate how many full blocks prefix has
        encrypted_empty = self.get_user_data('')
        encrypted_onechar = self.get_user_data('A' * self.keysize)
        prefix_full_block_count, start, stop, limit = 0, 0, self.keysize, math.floor(len(encrypted_empty) / self.keysize)
        while prefix_full_block_count < limit and encrypted_empty[start:stop] == encrypted_onechar[start:stop]:
            prefix_full_block_count, start, stop = prefix_full_block_count + 1, start + self.keysize, stop + self.keysize

        # Some magic happens and we find out the exact prefix length - not sure how it's work for CBC
        prefix_length = len('comment1=cooking%20MCs;userdata=')
        prefix_padding_length = prefix_length % self.keysize
        prefix_padding = 'A' * prefix_padding_length
        filled_blocks = 1 if prefix_padding_length > 0 else 0

        # now build the payload block
        payload = 'XadminYtrue'
        payload_padding = 'A' * (self.keysize - len(payload))
        full_payload = payload_padding + payload

        # positions in block for = and ;
        index_c1 = full_payload.index('X')
        index_c2 = full_payload.index('Y')

        # dummy block with all A's
        dummy_block = list('A' * self.keysize)

        # cipher-text
        encrypted_payload = bytearray(self.get_user_data(prefix_padding + "".join(dummy_block) + full_payload))
        # count the dummy block
        filled_blocks += 1

        # calculate absolute positions in the cipher-text of the replacements
        p1 = self.keysize * (prefix_full_block_count + filled_blocks - 1) + index_c1
        p2 = self.keysize * (prefix_full_block_count + filled_blocks - 1) + index_c2

        # perform the replace
        replace_c1 = encrypted_payload[p1] ^ ord('X') ^ ord(';')
        replace_c2 = encrypted_payload[p2] ^ ord('Y') ^ ord('=')
        encrypted_payload[p1] = replace_c1
        encrypted_payload[p2] = replace_c2

        # and poof
        if self.check_if_admin(bytes(encrypted_payload)):
            print_line('Success!', color=GREEN)
        else:
            print_line('Failed... try again', color=RED)

    def get_user_data(self, user_data):
        """
        Encrypted user profile
        :param user_data:
        :return:
        """
        user_data = 'comment1=cooking%20MCs;userdata=' + user_data.replace(';', '').replace('=', '') + ';comment2=%20like%20a%20pound%20of%20bacon'
        data = pkcs7_pad(user_data.encode(), len(self.key))
        return encrypt_aes_128_cbc(data, self.key, self.iv)

    def check_if_admin(self, encrypted):
        """
        Decrypt user profile and check if admin
        :param encrypted:
        :return:
        """
        decrypted = decrypt_aes_128_cbc(encrypted, self.key, self.iv)
        decrypted = decrypted.decode('iso-8859-1')
        parts = decrypted.split(';')
        for p in parts:
            (k, v) = p.split('=')
            if k == 'admin' and v == 'true':
                return True
        return False
