# img2rgb565

A simple Python tool to convert images to RGB565 format for use with embedded displays (e.g., ST7735) and generate either Arduino C arrays or raw binary files.

## Features
- Convert images to RGB565 format
- Output as Arduino C array or raw binary file
- Optional image resizing

## Requirements
- Python 3.8+
- [Pillow](https://pypi.org/project/Pillow/)
- [NumPy](https://pypi.org/project/numpy/)

Install dependencies:
```bash
pip install -r requiremenst.txt
```

## Usage

```bash
python img2rgb565.py <input_image> [--output <output_file>] [--resize WIDTH HEIGHT] [--name VAR_NAME]
```

- `<input_image>`: Path to the input image file (e.g., PNG, JPG).
- `--output`, `-o`: Output binary file (e.g., `image.bin`). If omitted, Arduino code is printed to stdout.
- `--resize WIDTH HEIGHT`: Resize the image to the specified dimensions before conversion.
- `--name VAR_NAME`: Variable name for the Arduino array (default: `my_image`).

## Examples

**Generate Arduino C array:**
```bash
python img2rgb565.py mypic.png --resize 128 160 --name mypic
```

**Generate binary file:**
```bash
python img2rgb565.py mypic.png --resize 128 160 --output mypic.bin
```

## Output
- **Arduino C array:** Prints a `const uint16_t` array and image dimensions for direct use in Arduino sketches.
- **Binary file:** Creates a `.bin` file with RGB565 data (big-endian) for direct upload to embedded devices.

## License

MIT License
