#!/usr/bin/env python3.9

import os
import random
import string

directory = 'hash_input'


def generate_random_file(file_name, file_size, buffer_size=50 * 1024 * 1024):
    """Generate a file with random content using a buffer."""
    chars = string.ascii_letters + string.digits
    with open(file_name, 'w') as f:
        while file_size > 0:
            chunk_size = min(buffer_size, file_size)
            f.write(''.join(random.choices(chars, k=chunk_size)))
            file_size -= chunk_size


def main():
    num_files = int(input("Enter the number of files to generate: "))

    if not os.path.isdir(directory):
        os.mkdir(directory)

    for i in range(num_files):
        file_size = int(input(f"Enter the size of file {i+1} in bytes: "))

        file_name = os.path.join(directory, f"file_{i + 1}_{file_size}.txt")
        generate_random_file(file_name, file_size)
        print(f"Generated {file_name}")


if __name__ == "__main__":
    main()
