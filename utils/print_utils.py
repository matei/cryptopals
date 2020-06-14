"""
Util functions for printing colorized messages and interacting with user
"""

import getpass
import sys

RED = '\033[0;31m'
GREEN = '\033[0;32m'
NC = '\033[0m'
CYAN = '\033[0;36m'
LGREEN = '\033[1;32m'
WHITE = '\u001b[37m'
BLUE = '\u001b[34m'

BOLD_START = '\033[1m'
BOLD_END ='\033[0m'


def get_reply(question, allowed_options):
    """
    Ask user a question and retrieve input
    Validate if input is in allowed_options (optionally, only if allowed_options is not empty)
    Return first letter of chosen option
    :param question: string
    :param allowed_options: list
    :return: char
    """
    reply = ""
    while len(reply) == 0 or reply.lower() not in allowed_options:
        reply = input(CYAN + question + NC)
        if len(allowed_options) == 0:
            break
    return reply.lower()


def get_full_reply(question):
    """
    Ask user a question and retrieve full reply
    :param question: string
    :return: string
    """
    reply = ""
    while len(reply) == 0:
        if 'password' in question.lower():
            reply = getpass.getpass(prompt=CYAN + question + NC)
        else:
            reply = input(CYAN + question + NC)
    return reply.strip()


def wait_for_enter(message):
    """
    Press enter to continue...
    :param message: string
    :return: string
    """
    getpass.getpass(prompt=CYAN + message + NC)


def print_debug(message, debug=True):
    """
    Print debug message
    :param message: string
    :param debug: bool
    :return:
    """
    if debug:
        sys.stdout.write(f'{LGREEN}*[DEBUG]: {message}{NC}\n')


def print_status(message, with_prefix=True):
    """
    Print status message
    :param with_prefix:
    :param message: string
    :return:
    """
    message = f'{CYAN}******* [Status] {message}{NC}\n' if with_prefix else f'{CYAN}{message}{NC}\n'
    sys.stdout.write(message)


def print_line(message, color=CYAN):
    """
    Print one line of text in cyan/red with no prefix
    :param color:
    :param message:
    :return:
    """
    sys.stdout.write(f'{color}{message}{NC}\n')


def print_error(message, with_prefix=True):
    """
    Print error message
    :param with_prefix:
    :param message: string
    :return:
    """
    message = f'{RED}* [Error] {message}{NC}\n' if with_prefix else f'{RED}{message}{NC}\n'
    sys.stderr.write(message)


def print_success(message):
    """
    Print success message
    :param message:
    :return:
    """
    sys.stdout.write(f'{GREEN}* [OK] {message}{NC}\n')