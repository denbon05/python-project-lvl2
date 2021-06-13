#!/usr/bin/env python
import argparse

from gendiff.app import generate_diff


def main():
    """Showing difference between two files."""
    parser = argparse.ArgumentParser(description="Generate diff")
    parser.add_argument("first_file", help="first file for compare")
    parser.add_argument("second_file", help="second file for compare")
    parser.add_argument(
        "-f", "--format", help="set format of output", default='stylish',
    )
    args = parser.parse_args()
    diff = generate_diff(args.first_file, args.second_file, args.format)
    print(diff)


if __name__ == '__main__':
    main()
