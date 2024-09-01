"""
Copyright (C) © 2024  Petr Alexandrovich Sabanov

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


import os


def get_directory_size(directory):
	total_size = 0
	for root, _, files in os.walk(directory):
		for file in files:
			filepath = os.path.join(root, file)
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