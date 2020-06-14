from cryptoutils.aes import generate_random_aes_key, encrypt_aes_128_ecb, decrypt_aes_128_ecb, pkcs7_pad
from utils.print_utils import *
from urllib.parse import parse_qsl


class Challenge13:

    def __init__(self):
        """
        Init
        """
        self.expected = 'role=admin'
        self.key = generate_random_aes_key()

    def display(self):
        """
        Display challenge info
        :return:
        """
        print_line(f'{BOLD_START}ECB cut-and-paste{BOLD_END}', color=BLUE)
        print_line('Write a k=v parsing routine, as if for a structured cookie. The routine should take: ', color=BLUE)
        print_line('foo=bar&baz=qux&zap=zazzle', color=WHITE)
        print_line('and parse it', color=BLUE)
        print_line('Now write a function that encodes a user profile in that format, given an email address.', color=BLUE)
        print_line('profile_for("foo@bar.com")', color=WHITE)
        print_line('... and it should produce: ', color=BLUE)
        print_line('email=foo@bar.com&uid=10&role=user', color=WHITE)
        print_line('Your "profile_for" function should not allow encoding metacharacters (& and =). ', color=BLUE)
        print_line('Now, two more easy functions. Generate a random AES key, then: ', color=BLUE)
        print_line('A. Encrypt the encoded user profile under the key; "provide" that to the "attacker".', color=BLUE)
        print_line('B. Decrypt the encoded user profile and parse it.', color=BLUE)
        print_line('Using only the user input to profile_for() (as an oracle to generate "valid" ciphertexts) and the ciphertexts themselves, make a role=admin profile', color=BLUE)

    def run(self):
        """
        By controlling email length, align role value to start of block. Get last block (which is encrypted "admin" + padding)
        and stitch that with first part which will end with "role="
        Then replace that block with payload block which is calculated using same encryption function
        :return:
        """
        email = 't1234@est.com'
        profile_encrypted = self.encode_profile_encrypted(email)
        first_part = profile_encrypted[0:32]
        email = 't124@e.comadmin'
        admin = self.encode_profile_encrypted(email)[16:32]
        stitched = first_part + admin
        email, uid, role = self.decrypt_profile(stitched)
        color = GREEN if role == 'admin' else RED
        print_line(f'Email is {email} and uid is {uid} and role is {role}', color=color)

    def encode_profile_encrypted(self, email, uid=10, role='admin'):
        """
        Encrypt user profile
        :param email:
        :param uid:
        :param role:
        :return:
        """
        return encrypt_aes_128_ecb(pkcs7_pad(encode_profile(email, uid, role).encode(), 16), self.key)

    def decrypt_profile(self, encrypted_bytes):
        """
        Decrypt user profile
        :param encrypted_bytes:
        :return:
        """
        parsed = parse_cookie(decrypt_aes_128_ecb(encrypted_bytes, self.key).decode())
        return parsed['email'], parsed['uid'], parsed['role']


def encode_profile(email, uid=10, role='user'):
    """
    Encvode user profile
    :param email:
    :param uid:
    :param role:
    :return:
    """
    email = email.replace('=', '')
    email = email.replace('&', '')
    return f'email={email}&uid={uid}&role={role}'


def parse_cookie(cookie_string):
    return {k: v for k, v in parse_qsl(cookie_string)}