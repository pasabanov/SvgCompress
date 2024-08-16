import os
import re
import argparse


parser = argparse.ArgumentParser(description="Compress SVG files by removing unnecessary whitespace and comments.")
parser.add_argument('paths', nargs='+', help='List of directories or SVG files to compress.')
parser.add_argument('-r', '--recursive', action='store_true', help='Recursively process directories.')
parser.add_argument('-v', '--version', action='version', version='SVG Compressor 1.0', help='Show the version of the script.')
parser.add_argument('--new-version', default='auto', help='Set a new version for the SVG files. Options: "text" (e.g., "1.1"), "auto", "" (empty string to remove version).')

args = parser.parse_args()


#def update_version(content):
	## Regular expression to find the version attribute
	#version_pattern = r'(<svg[^>]*\bversion=")([^"]*)(")'

	#if args.new_version == '':
		## Remove the version attribute
		#content = re.sub(version_pattern, r'\1\3', content)
	#elif args.new_version == 'auto':
		## Automatically increment the last number of the version by one
		#match = re.search(version_pattern, content)
		#if match:
			#current_version = match.group(2)
			## Split the version into parts and increment the last part
			#version_parts = current_version.split('.')
			#if version_parts[-1].isdigit():
				#version_parts[-1] = str(int(version_parts[-1]) + 1)
			#else:
				#version_parts.append('1')
			#args.new_version = '.'.join(version_parts)
			#content = re.sub(version_pattern, rf'\1{args.new_version}\3', content)
		#else:
			## If the version attribute is not found, add it
			#content = re.sub(r'<svg', r'<svg version="1.0"', content)
	#else:
		## Set the specified version
		#content = re.sub(version_pattern, rf'\1{args.new_version}\3', content)
		#if re.search(r'<svg[^>]*\bversion="[^"]*"', content) is None:
			## If the version attribute was not found, add it
			#content = re.sub(r'<svg', rf'<svg version="{args.new_version}"', content)

	#return content


def compress_svg(content):

	# Deleting whitespace at the ends
	content = content.strip()

	## Update version
	#content = update_version(content)

	# If there is no xlink use, delete redundant attribute
	if re.search(r'xlink:href', content) is None:
		content = re.sub(r'\s+xmlns:xlink="[^"]+"', '', content)

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


def main():
	for path in args.paths:
		if os.path.isfile(path) and path.endswith('.svg'):
			process_file(path)
		elif os.path.isdir(path):
			process_directory(path)
		else:
			print(f"Warning: {path} is neither a file nor a directory, or not an SVG file.")


if __name__ == '__main__':
	main()