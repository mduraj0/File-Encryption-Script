import argparse, getpass
import pathlib
from argparse import ArgumentParser, Namespace
from typing import Sequence
from encryption import Encryption, Decryption
from cryptography.fernet import InvalidToken
from time import time
from tqdm import tqdm


class Password(argparse.Action):
    def __call__(self, parser, namespace, values, optional_string):
        if values is None:
            values = getpass.getpass()

        setattr(namespace, self.dest, values)


def file_name(value: str):
    if value.endswith(('.txt', '.dokodu')):
        return value
    raise argparse.ArgumentError()


def main(args):
    try:
        file_to_process = args.file
        if args.verbose >= 3:
            file_to_process = tqdm(args.file)

        for file in file_to_process:
            before = time()
            path = pathlib.Path(file)
            if args.mode == 'encrypt':
                action = Encryption(path)
            elif args.mode == 'decrypt':
                action = Decryption(path)

            action.execute(args.password)
            after = time()
            if 0 < args.verbose <= 2:
                print(file, end= ' ')
                if args.verbose > 1:
                    print(f'Time : {after - before}')
                print()

            if args.verbose >= 3:
                file_to_process.set_description(file)
    except InvalidToken:
        print('Bad password!! ERROR')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Decrypt encrypt app')
    parser.add_argument(
        '-m',
        '--mode',
        choices=['encrypt', 'decrypt', 'append'],
        required=True,
        help='''encrypt --- encrypt file
    decrypt --- decrypt file
    append --- append text to encrypted file'''
    )

    parser.add_argument(
        '-p',
        '--password',
        required=True,
        nargs='?',
        dest='password',
        action=Password
    )

    parser.add_argument('-v', '--verbose', action='count', default=0)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-f', '--file', action='append', type=file_name, help='list of files to process.')
    group.add_argument('-d', '--dir', help='path to folder with file to process')

    args = parser.parse_args()
    main(args)
