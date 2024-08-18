# SvgCompress

## Description

`SvgCompress` is a tool for compressing SVG files by removing unnecessary whitespace, comments, and optional attributes. It also supports optimization with [SVGO](https://github.com/svg/svgo) and compression into [SVGZ](https://ru.wikipedia.org/wiki/SVG#SVGZ). The tool helps reduce the file size and clean up SVG files for better performance and preparing for release versions.

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/pasabanov/SvgCompress
    cd SvgCompress
    ```

2. **(Optional) If you want to use `--svgo` option, make sure [SVGO](https://github.com/svg/svgo) is installed.**

3. **(Optional) If you want to use `--svgz` option, make sure [gzip](https://www.gnu.org/software/gzip/) is installed.**

## Usage

To compress SVG files, run the script with the following command:

```sh
python compress-svg.py [options] paths
```

## Options

`-h`, `--help` Show this help message and exit  
`-v`, `--version` Show the version of the script  
`-r`, `--recursive` Recursively process directories  
`-f`, `--remove-fill` Remove `fill="..."` attributes  
`--svgo` Use [SVGO](https://github.com/svg/svgo) if it exists in the system  
`--svgz` Compress to [.svgz](https://ru.wikipedia.org/wiki/SVG#SVGZ) format with [gzip](https://www.gnu.org/software/gzip/) utility after processing

## Examples
1. Compress a single SVG file:
    ```sh
    python compress-svg.py my-icon.svg
    ```
2. Compress all SVG files in some directories and files:
    ```sh
    python compress-svg.py my-icons-directory1 my-icon.svg directory2 icon2.svg
    ```
3. Compress all SVG files in a directory and all subdirectories:
    ```sh
    python compress-svg.py -r my-icons-directory
   ```
4. Compress a SVG file removing every `fill=...` attribute in it (making it monocolor):
    ```sh
    python compress-svg.py -f my-icon.svg
    ```
5. Using `ls-sizes.py` to compare the sizes:
    ```sh
    cp -r icons/ compressed-icons/
    python compress-svg.py [options] compressed-icons
    python ls-sizes.py
    ```

## License

This project is licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0).

You are free to:
- Share — copy and redistribute the material in any medium or format
- Adapt — remix, transform, and build upon the material

Under the following terms:
- **Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.

For more details, see the full license at https://creativecommons.org/licenses/by/4.0/

## Copyright
2024 Petr Alexandrovich Sabanov