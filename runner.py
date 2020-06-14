import argparse
import os
from utils.print_utils import *


class Runner:
    """
    Collect challenge files and display runner menu
    """

    def __init__(self, base_path):
        """
        Init
        :param base_path: path to project root
        """
        self.path = base_path
        self.sets = {}
        self.python_extension = '.py'
        self.challenge_index, self.challenge_counter = {}, 0
        self.challenge_dir = os.path.join(self.path, 'challenges')
        self.collect_challenges()

    def choose_challenge(self):
        """
        Show challenge choice menu and ask for choice
        :return:
        """
        print_line('CryptoPals Challenges Runner')
        print_line('--------[ by Matei ]---------', color=RED)
        k = 1
        for set_name, challenges in self.sets.items():
            set_display = file_name_to_title(set_name)
            print_line(set_display, color=LGREEN)
            print_line('-' * len(set_display), color=LGREEN)
            for challenge in challenges:
                print_line(f'[{k}] {file_name_to_title(challenge)}')
                k += 1
        print_line('[0] to quit')
        self.run(int(get_reply('Enter number of challenge to run: ', [str(i) for i in range(0, k + 1)])))

    def run(self, option):
        """
        Run selected menu option
        :param option:
        :return:
        """
        if option == 0:
            print_success('Exiting...')
            exit(0)
        else:
            print_line('')
            challenge = challenge_instance(self.challenge_index[option]['set'], self.challenge_index[option]['challenge'])
            challenge.display()
            challenge.run()
            wait_for_enter('Press enter to continue...')
            print_line('')
            self.choose_challenge()

    def collect_challenges(self):
        """
        Go through set* subdirectories from challenges dir and collect individual challenge files
        :return:
        """
        for set_dir in [d for d in os.listdir(self.challenge_dir) if os.path.isdir(os.path.join(self.challenge_dir, d))]:
            self.collect_set(set_dir)

    def collect_set(self, set_name):
        """
        Collect list of challenges from set dir
        :param set_name:
        :return:
        """
        prefix, extension = 'challenge_', '.py'
        challenges = []
        for file in sorted(os.listdir(os.path.join(self.challenge_dir, set_name))):
            if file[:len(prefix)] == prefix and file[-len(extension):] == extension:
                challenges.append(file)
                self.challenge_counter += 1
                self.challenge_index[self.challenge_counter] = {'set': set_name, 'challenge': file}
        if len(challenges):
            self.sets[set_name] = challenges


def challenge_instance(set_name, challenge_name):
    """
    Get instance of challenge class based on set and filename
    :param set_name:
    :param challenge_name:
    :return:
    """
    class_name = ''.join(challenge_name.split('_')[0:2]).title()
    package_name = '.'.join(['challenges', set_name, without_extension(challenge_name)])
    module = __import__(package_name, fromlist=[class_name])
    challenge_class = getattr(module, class_name)
    return challenge_class()


def without_extension(filename):
    """
    Return filename without python extension
    :param filename:
    :return:
    """
    python_extension = '.py'
    if filename[-len(python_extension):] != python_extension:
        return filename
    return filename[:-len(python_extension)]


def file_name_to_title(filename):
    """
    Transform filename to menu item
    :param filename:
    :return:
    """
    return ' '.join(word.title() for word in without_extension(filename).split('_'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Runner')
    parser.add_argument('--path', required=False, default='.')
    args = parser.parse_args()
    runner = Runner(args.path)
    runner.choose_challenge()
