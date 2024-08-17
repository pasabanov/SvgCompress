"""
© 2024 Petr Alexandrovich Sabanov. This code is licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0).

You are free to:
- Share — copy and redistribute the material in any medium or format
- Adapt — remix, transform, and build upon the material

You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.

For full license details, see https://creativecommons.org/licenses/by/4.0/
"""


import argparse
import os
import re
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


RE_FILL = re.compile(r'fill="[^"]*"')
RE_XLINK_HREF = re.compile(r'xlink:href')
RE_XMLNS_XLINK = re.compile(r'\s+xmlns:xlink="[^"]*"')
RE_COMMENT = re.compile(r'<!--.*?-->', flags=re.DOTALL)
RE_XML_TAG = re.compile(r'<\?xml.*?>', flags=re.DOTALL)
RE_DOCTYPE_SVG = re.compile(r'<!DOCTYPE svg[^>]*>')
RE_WHITESPACE = re.compile(r'\s+')
RE_WHITESPACE_AROUND_TAGS = re.compile(r'\s*(<|>)\s*')
RE_SYMBOLS_BETWEEN_TAGS = re.compile(r'>[^<]+<')
RE_XML_SPACE = re.compile(r'\s+xml:space="[^"]+"')


def compress_svg_content(content):
	# Deleting whitespace at the ends
	content = content.strip()
	if args.remove_fill:
		content = RE_FILL.sub('', content)
	# If there is no xlink use, delete redundant attribute
	if RE_XLINK_HREF.search(content) is None:
		content = RE_XMLNS_XLINK.sub('', content)
	# Deleting comments
	content = RE_COMMENT.sub('', content)
	# Deleting "<?xml" tag
	content = RE_XML_TAG.sub('', content)
	# Deleting "<!DOCTYPE svg" tag
	content = RE_DOCTYPE_SVG.sub('', content)
	# Replacing whitespace with single space
	content = RE_WHITESPACE.sub(' ', content)
	# Removing spaces between angle brackets
	content = RE_WHITESPACE_AROUND_TAGS.sub(r'\1', content)
	# If there are no other symbols between angle brackets, delete redundant attribute
	if RE_SYMBOLS_BETWEEN_TAGS.search(content) is None:
		content = RE_XML_SPACE.sub('', content)
	return content


def process_file(filepath):
	with open(filepath, 'r', encoding='utf-8') as file:
		content = file.read()
	compressed_content = compress_svg_content(content)
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