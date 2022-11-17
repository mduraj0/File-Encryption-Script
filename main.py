import argparse


def file_name(value: str):
    if value.endswith('.txt'):
        return value
    raise argparse.ArgumentError()


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
    '-p'
)

parser.add_argument('-v', '--verbose', action='count', default=0)
group = parser.add_mutually_exclusive_group()
group.add_argument('-f', '--file', action='append', type=file_name, help='list of files to process.')
group.add_argument('-d', '--dir', help='path to folder with file to process')

args = parser.parse_args()
print(args)
