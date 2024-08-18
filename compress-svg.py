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


def default_optimize(filepath: str, remove_fill: bool):

	# Define regular expressions once and store them as attributes of the function
	if not hasattr(default_optimize, 'RE_FILL'):
		default_optimize.RE_FILL = re.compile(r'fill="[^"]*"')
		default_optimize.RE_XLINK_HREF = re.compile(r'xlink:href')
		default_optimize.RE_XMLNS_XLINK = re.compile(r'\s+xmlns:xlink="[^"]*"')
		default_optimize.RE_COMMENT = re.compile(r'<!--.*?-->', flags=re.DOTALL)
		default_optimize.RE_XML_TAG = re.compile(r'<\?xml.*?>', flags=re.DOTALL)
		default_optimize.RE_DOCTYPE_SVG = re.compile(r'<!DOCTYPE svg[^>]*>')
		default_optimize.RE_WHITESPACE = re.compile(r'\s+')
		default_optimize.RE_WHITESPACE_AROUND_TAGS = re.compile(r'\s*([<>])\s*')
		default_optimize.RE_SYMBOLS_BETWEEN_TAGS = re.compile(r'>[^<]+<')
		default_optimize.RE_XML_SPACE = re.compile(r'\s+xml:space="[^"]+"')

	with open(filepath, 'r', encoding='utf-8') as file:
		content = file.read()

	# Removing leading and trailing whitespace
	content = content.strip()
	# If remove_fill is set, removing "fill" attributes
	if remove_fill:
		content = default_optimize.RE_FILL.sub('', content)
	# If there is no xlink use, removing redundant "xmlns:xlink" attribute
	if default_optimize.RE_XLINK_HREF.search(content) is None:
		content = default_optimize.RE_XMLNS_XLINK.sub('', content)
	# Removing comments
	content = default_optimize.RE_COMMENT.sub('', content)
	# Removing "<?xml" tag
	content = default_optimize.RE_XML_TAG.sub('', content)
	# Removing "<!DOCTYPE svg" tag
	content = default_optimize.RE_DOCTYPE_SVG.sub('', content)
	# Replacing whitespace with single space
	content = default_optimize.RE_WHITESPACE.sub(' ', content)
	# Removing spaces around angle brackets
	content = default_optimize.RE_WHITESPACE_AROUND_TAGS.sub(r'\1', content)
	# If there are no other symbols between angle brackets, removing redundant "xml:space" attribute
	if default_optimize.RE_SYMBOLS_BETWEEN_TAGS.search(content) is None:
		content = default_optimize.RE_XML_SPACE.sub('', content)

	with open(filepath, 'w', encoding='utf-8') as file:
		file.write(content)


def compress_to_svgz(filepath: str, gzip_path: str):
	# Assuming that file ends with '.svg', so we add 'z' to get '.svgz'
	svgz_filepath = f'{filepath}z'
	try:
		with open(filepath, 'rb') as f_in:
			with open(svgz_filepath, 'wb') as f_out:
				subprocess.run([gzip_path, '-c', '-9'], stdin=f_in, stdout=f_out, check=True)
		os.remove(filepath)
	except subprocess.CalledProcessError as e:
		print(f'Error compressing {filepath} to .svgz: {e}', file=stderr)


def find_svg_files(path: str, recursive: bool):
	if os.path.isfile(path) and path.endswith('.svg'):
		return [path]
	elif not os.path.isdir(path):
		print(f'Error: {path} is neither an SVG file nor a directory.', file=stderr)
		return []
	svg_files = []
	for root, _, files in os.walk(path):
		for filename in files:
			if filename.endswith('.svg'):
				svg_files.append(os.path.join(root, filename))
		if not recursive:
			break
	return svg_files


def main():
	parser = argparse.ArgumentParser(description='Compress SVG files by removing unnecessary whitespace, comments, metadata and some other data.')
	parser.add_argument('paths', nargs='+', help='List of directories or SVG files to compress.')
	parser.add_argument('-v', '--version', action='version', version='SVG Compressor 1.0', help='Show the version of the script.')
	parser.add_argument('-r', '--recursive', action='store_true', help='Recursively process directories.')
	parser.add_argument('-f', '--remove-fill', action='store_true', help='Remove fill="..." attributes.')
	parser.add_argument('--svgo', action='store_true', help='Use svgo if it exists in the system.')
	parser.add_argument('--svgz', action='store_true', help='Compress to .svgz format with gzip utility after processing.')
	parser.add_argument('--no-default', action='store_true', help='Skip default optimizations.')

	args = parser.parse_args()

	svgo_path = shutil.which('svgo') if args.svgo else None
	gzip_path = shutil.which('gzip') if args.svgz else None

	if args.svgo and not svgo_path:
		print('Error: svgo executable not found in the system.', file=stderr)
	if args.svgz and not gzip_path:
		print('Error: gzip executable not found in the system.', file=stderr)

	if args.no_default and not svgo_path and not gzip_path:
		# There is nothing to do
		return

	svg_files = list(set(file for path in args.paths for file in find_svg_files(path, args.recursive)))

	if not args.no_default:
		for file in svg_files:
			default_optimize(file, args.remove_fill)

	if args.svgo and svgo_path:
		svgo_arguments = [svgo_path, '-q'] + svg_files
		try:
			subprocess.run(svgo_arguments, check=True)
			subprocess.run(svgo_arguments, check=True) # Second time for additional optimization
		except subprocess.CalledProcessError as e:
			print(f'Error during SVGO optimization for files {svg_files}: {e}', file=stderr)

	if args.svgz and gzip_path:
		for file in svg_files:
			compress_to_svgz(file, gzip_path)


if __name__ == '__main__':
	main()