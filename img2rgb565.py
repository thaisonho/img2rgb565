from PIL import Image
import numpy as np
import argparse

def i2rgb565(image_path, resize_dim=None):
    try:
        with Image.open(image_path) as img:
            img = img.convert('RGB')
            if resize_dim:
                img = img.resize(resize_dim)
            
            rgb_array = np.array(img, dtype=np.uint8)

            r = (rgb_array[:, :, 0] >> 3).astype(np.uint16)
            g = (rgb_array[:, :, 1] >> 2).astype(np.uint16)
            b = (rgb_array[:, :, 2] >> 3).astype(np.uint16)
            rgb565 = (r << 11) | (g << 5) | b
            return rgb565, (img.width, img.height)
    except Exception as e:
        print(f"Error occur: {e}")
        return None, None
    
def gen_arduino_code(rgb565, dim, var_name):
    width, height = dim
    flat_data = rgb565.flatten()

    print(f'const uint16_t {var_name}[{len(flat_data)}] = {{')

    for i in range(0, len(flat_data), 16):
        chunk = flat_data[i:i+16]
        hex_chunk = ', '.join(f'0x{val:04X}' for val in chunk)
        print(f'    {hex_chunk},')
    print('};')
    print(f'int16_t {var_name}_width = {width};\nint16_t {var_name}_height = {height};')
    
def gen_bin_file(rgb565, filename):
    # big endian conversion
    rgb565_data = rgb565.byteswap()
    with open(filename, 'wb') as f:
        f.write(rgb565_data.tobytes())
    print(f'Binary file {filename} created successfully.')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Convert an image to RGB565 format for ST7735 displays.'
    )
    parser.add_argument('input_image', type=str, help='Path to the input image file.')
    parser.add_argument(
        '--output',
        '-o',
        help='The output binary file (e.g., image.bin). If not provided, Arduino code will be generated.'
    )
    parser.add_argument(
        '--resize',
        nargs=2,
        type=int,
        metavar=('WIDTH', 'HEIGHT'),
        help='Resize the image to the specified dimensions.'
    )
    parser.add_argument(
        '--name',
        default='my_image',
        help='Variable name for the Arduino array (default: my_image).'
    )

    args = parser.parse_args()

    resize_dimensions = tuple(args.resize) if args.resize else None
    rgb565_array, dims = i2rgb565(args.input_image, resize_dimensions)

    if rgb565_array is not None:
        if args.output:
            gen_bin_file(args.output, rgb565_array)
        else:
            gen_arduino_code(rgb565_array, dims, args.name)