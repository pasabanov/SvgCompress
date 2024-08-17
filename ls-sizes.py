"""
© 2024 Petr Alexandrovich Sabanov. This code is licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0).

You are free to:
- Share — copy and redistribute the material in any medium or format
- Adapt — remix, transform, and build upon the material

You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.

For full license details, see https://creativecommons.org/licenses/by/4.0/
"""


import os


def get_directory_size(directory):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            # Check if it's a file and calculate its size
            if os.path.isfile(filepath):
                total_size += os.path.getsize(filepath)
    return total_size


def list_directory_with_size(directory):
    items = os.listdir(directory)
    items.sort()  # Sort for a more ls-like output

    # First pass: calculate the max lengths
    max_name_length = max(len(item) for item in items)
    max_size_length = 0

    sizes = []
    for item in items:
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            size = os.path.getsize(item_path)
        elif os.path.isdir(item_path):
            size = get_directory_size(item_path)
        else:
            size = 0  # Handle non-regular files if needed

        sizes.append(size)
        max_size_length = max(max_size_length, len(str(size)))

    # Second pass: print with correct alignment
    for item, size in zip(items, sizes):
        print(f"{item:<{max_name_length}} {size:>{max_size_length}}")


def main():
    current_directory = os.getcwd()
    list_directory_with_size(current_directory)


if __name__ == "__main__":
    main()