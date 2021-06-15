#!/usr/bin/env python
import argparse

from gendiff.app import generate_diff


def main():
    """Showing difference between two files."""
    parser = argparse.ArgumentParser(
        description="Compares two configuration files and shows a difference.",
    )
    parser.add_argument("filepaht1", help="first file for compare")
    parser.add_argument("filepath2", help="second file for compare")
    parser.add_argument(
        "-f", "--format", help="set format of output", default='stylish',
    )
    args = parser.parse_args()
    diff = generate_diff(args.filepaht1, args.filepath2, args.format)
    print(diff)


if __name__ == '__main__':
    main()
