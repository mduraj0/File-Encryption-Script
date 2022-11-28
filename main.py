import argparse, getpass
import pathlib
from os import walk
from argparse import ArgumentParser, Namespace
from typing import Sequence
from encryption import Encryption, Decryption, Append
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


def list_files_in_directory(dirname: str):
    file_to_process = []
    for path, dirs, files in walk(args.dir):
        for file in files:
            if file.endswith(('.txt', '.dokodu')):
                file_to_process.append(f'{path}\{file}')

    return file_to_process


def main(args):
    try:
        if args.dir:
            file_to_process = list_files_in_directory(args.dir)
        elif args.file:
            file_to_process = args.file
        else:
            raise argparse.ArgumentError()

        if args.verbose >= 3:
            file_to_process = tqdm(args.file)

        for file in file_to_process:
            before = time()
            path = pathlib.Path(file)
            if args.mode == 'encrypt':
                action = Encryption(path, args.password)
            elif args.mode == 'decrypt':
                action = Decryption(path, args.password)
            elif args.mode == 'append':
                text = input('What you want to append to file?')
                action = Append(path, args.password, text)

            action.start()
            after = time()
            if 0 < args.verbose <= 2:
                print(file, end=' ')
                if args.verbose > 1:
                    print(f'Time : {after - before}')
                print()

            if args.verbose >= 3:
                file_to_process.set_description(file)
    except InvalidToken:
        print('Bad password!! ERROR')
    except argparse.ArgumentError:
        print('Bad file or dir name!! ERRORR')


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
    group.add_argument('-f', '--file',
                       action='append',
                       type=file_name,
                       help='list of files to process.')
    group.add_argument('-d', '--dir', help='path to folder with file to process')

    args = parser.parse_args()
    main(args)
