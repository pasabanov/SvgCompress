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

from sys import stderr


args = None
svgo_path = None
gzip_path = None


def parse_arguments():
	global args, svgo_path, gzip_path
	parser = argparse.ArgumentParser(description='Compress SVG files by removing unnecessary whitespace and comments.')
	parser.add_argument('paths', nargs='+', help='List of directories or SVG files to compress.')
	parser.add_argument('-v', '--version', action='version', version='SVG Compressor 1.0', help='Show the version of the script.')
	parser.add_argument('-r', '--recursive', action='store_true', help='Recursively process directories.')
	parser.add_argument('-f', '--remove-fill', action='store_true', help='Remove fill="..." attributes.')
	parser.add_argument('--svgo', action='store_true', help='Use svgo if it exists in the system.')
	parser.add_argument('--svgz', action='store_true', help='Compress to .svgz format with gzip utility after processing.')
	args = parser.parse_args()
	if args.svgo:
		svgo_path = shutil.which('svgo')
	if args.svgz:
		gzip_path = shutil.which('gzip')


def simple_compress(filepath):

	# Define regular expressions once and store them as attributes of the function
	if not hasattr(simple_compress, 'RE_FILL'):
		simple_compress.RE_FILL = re.compile(r'fill="[^"]*"')
		simple_compress.RE_XLINK_HREF = re.compile(r'xlink:href')
		simple_compress.RE_XMLNS_XLINK = re.compile(r'\s+xmlns:xlink="[^"]*"')
		simple_compress.RE_COMMENT = re.compile(r'<!--.*?-->', flags=re.DOTALL)
		simple_compress.RE_XML_TAG = re.compile(r'<\?xml.*?>', flags=re.DOTALL)
		simple_compress.RE_DOCTYPE_SVG = re.compile(r'<!DOCTYPE svg[^>]*>')
		simple_compress.RE_WHITESPACE = re.compile(r'\s+')
		simple_compress.RE_WHITESPACE_AROUND_TAGS = re.compile(r'\s*(<|>)\s*')
		simple_compress.RE_SYMBOLS_BETWEEN_TAGS = re.compile(r'>[^<]+<')
		simple_compress.RE_XML_SPACE = re.compile(r'\s+xml:space="[^"]+"')

	with open(filepath, 'r', encoding='utf-8') as file:
		content = file.read()

	# Deleting whitespace at the ends
	content = content.strip()
	if args.remove_fill:
		content = simple_compress.RE_FILL.sub('', content)
	# If there is no xlink use, delete redundant attribute
	if simple_compress.RE_XLINK_HREF.search(content) is None:
		content = simple_compress.RE_XMLNS_XLINK.sub('', content)
	# Deleting comments
	content = simple_compress.RE_COMMENT.sub('', content)
	# Deleting "<?xml" tag
	content = simple_compress.RE_XML_TAG.sub('', content)
	# Deleting "<!DOCTYPE svg" tag
	content = simple_compress.RE_DOCTYPE_SVG.sub('', content)
	# Replacing whitespace with single space
	content = simple_compress.RE_WHITESPACE.sub(' ', content)
	# Removing spaces around angle brackets
	content = simple_compress.RE_WHITESPACE_AROUND_TAGS.sub(r'\1', content)
	# If there are no other symbols between angle brackets, delete redundant attribute
	if simple_compress.RE_SYMBOLS_BETWEEN_TAGS.search(content) is None:
		content = simple_compress.RE_XML_SPACE.sub('', content)

	with open(filepath, 'w', encoding='utf-8') as file:
		file.write(content)


def compress_to_svgz(filepath):
	if not args.svgz or gzip_path is None:
		return
	if not filepath.endswith('.svg'):
		return
	svgz_filepath = f'{filepath}z'
	try:
		with open(filepath, 'rb') as f_in:
			with open(svgz_filepath, 'wb') as f_out:
				subprocess.run([gzip_path, '-c', '-9'], stdin=f_in, stdout=f_out, check=True)
		os.remove(filepath)
	except subprocess.CalledProcessError as e:
		print(f'Error compressing {filepath} to .svgz: {e}', file=stderr)


def traverse_directory(directory, target_function):
	for root, _, files in os.walk(directory):
		for filename in files:
			if filename.endswith('.svg'):
				filepath = os.path.join(root, filename)
				target_function(filepath)
		if not args.recursive:
			break


def process_path(path):
	if os.path.isfile(path) and path.endswith('.svg'):
		is_directory = False
	elif os.path.isdir(path):
		is_directory = True
	else:
		print(f'Error: {path} is neither an SVG file nor a directory.', file=stderr)
		return

	if is_directory:
		traverse_directory(path, simple_compress)
	else:
		simple_compress(path)

	if args.svgo and svgo_path is not None:
		svgo_arguments = [svgo_path, '-q', path]
		if is_directory and args.recursive:
			svgo_arguments.append('-r')
		try:
			subprocess.run(svgo_arguments, check=True)
			subprocess.run(svgo_arguments, check=True) # Second time for additional optimization
		except subprocess.CalledProcessError as e:
			print(f'Error during SVGO optimization for {path}: {e}', file=stderr)

	if args.svgz and gzip_path is not None:
		if is_directory:
			traverse_directory(path, compress_to_svgz)
		else:
			compress_to_svgz(path)


def main():
	if args.svgo and svgo_path is None:
		print('Error: svgo executable not found in the system.', file=stderr)
	if args.svgz and gzip_path is None:
		print('Error: gzip executable not found in the system.', file=stderr)
	for path in args.paths:
		process_path(path)


if __name__ == '__main__':
	parse_arguments()
	main()