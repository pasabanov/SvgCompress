"""
© 2024 Petr Alexandrovich Sabanov. This code is licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0).

You are free to:
- Share — copy and redistribute the material in any medium or format
- Adapt — remix, transform, and build upon the material

You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.

For full license details, see https://creativecommons.org/licenses/by/4.0/
"""


import os
import re
import argparse
import shutil
import subprocess


args = None
svgo_path = None


def parse_arguments():
	global args, svgo_path
	parser = argparse.ArgumentParser(description="Compress SVG files by removing unnecessary whitespace and comments.")
	parser.add_argument('paths', nargs='+', help='List of directories or SVG files to compress.')
	parser.add_argument('-v', '--version', action='version', version='SVG Compressor 1.0', help='Show the version of the script.')
	parser.add_argument('-r', '--recursive', action='store_true', help='Recursively process directories.')
	parser.add_argument('-f', '--remove-fill', action='store_true', help='Remove fill="..." attributes.')
	parser.add_argument('--svgo', action='store_true', help='Use svgo if it exists in the system.')
	args = parser.parse_args()
	if args.svgo:
		svgo_path = shutil.which('svgo')


def compress_svg(content):
	# Deleting whitespace at the ends
	content = content.strip()
	if args.remove_fill:
		content = re.sub(r'fill="[^"]*"', '', content)
	# If there is no xlink use, delete redundant attribute
	if re.search(r'xlink:href', content) is None:
		content = re.sub(r'\s+xmlns:xlink="[^"]*"', '', content)
	# Deleting comments
	content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
	# Deleting "<?xml" tag
	content = re.sub(r'<\?xml.*?>', '', content)
	# Deleting "<!DOCTYPE svg" tag
	content = re.sub(r'<!DOCTYPE svg[^>]*>', '', content)
	# Replacing whitespace with single space
	content = re.sub(r'\s+', ' ', content)
	# Removing spaces between angle brackets
	content = re.sub(r'\s*(<|>)\s*', r'\1', content)
	# If there are no other symbols between angle brackets, delete redundant attribute
	if re.search(r'>[^<]+<', content) is None:
		content = re.sub(r'\s+xml:space="[^"]+"', '', content)
	return content


def process_file(filepath):
	with open(filepath, 'r', encoding='utf-8') as file:
		content = file.read()
	compressed_content = compress_svg(content)
	with open(filepath, 'w', encoding='utf-8') as file:
		file.write(compressed_content)


def process_directory(directory):
	for root, _, files in os.walk(directory):
		for filename in files:
			if filename.endswith('.svg'):
				filepath = os.path.join(root, filename)
				process_file(filepath)
		if not args.recursive:
			break


def process_path(path):
	if os.path.isfile(path) and path.endswith('.svg'):
		is_directory = False
	elif os.path.isdir(path):
		is_directory = True
	else:
		print(f"Warning: {path} is neither an SVG file nor a directory.")
		return

	if is_directory:
		process_directory(path)
	else:
		process_file(path)

	if args.svgo and svgo_path is not None:
		svgo_arguments = [svgo_path, '-q', path]
		if is_directory and args.recursive:
			svgo_arguments.append('-r')
		try:
			subprocess.run(svgo_arguments, check=True)
			subprocess.run(svgo_arguments, check=True) # Second time for additional optimization
		except subprocess.CalledProcessError as e:
			print(f'Error during SVGO optimization for {path}: {e}')


def main():
	if args.svgo and svgo_path is None:
		print("Error: svgo executable not found in the system.")
	for path in args.paths:
		process_path(path)


if __name__ == '__main__':
	parse_arguments()
	main()