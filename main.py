import argparse


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

group = parser.add_mutually_exclusive_group()
group.add_argument('-f', '--file', action='append')

args = parser.parse_args()
print(args)