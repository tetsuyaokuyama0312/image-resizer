"""
This module resizes image files.
"""

import argparse
import os

from PIL import Image

DEFAULT_OUT_DIR = './output/'
DEFAULT_OUT_EXT = '.png'
DEFAULT_WIDTH = 1024
DEFAULT_HEIGHT = 1024


def resize_all(files: list, out_dir: str = DEFAULT_OUT_DIR, out_ext: str = DEFAULT_OUT_EXT,
               width: str = DEFAULT_WIDTH,
               height: str = DEFAULT_HEIGHT,
               callback=None):
    """
    Resizes image files.
    Output file name is determined by input file name and out_ext.
    Callback function(callback) is called every time one task is completed.

    :param files: image file name to resize
    :param out_dir: output files directory
    :param out_ext: extension of resized image file
    :param width:  width(px) of resized image file
    :param height: height(px) of resized image file
    :param callback: callback function that is called every time one task is completed
    """
    for file in files:
        resize(file, out_dir, out_ext, width, height)
        if callback:
            callback()


def resize(file: str, out_dir: str = DEFAULT_OUT_DIR, out_ext: str = DEFAULT_OUT_EXT, width: str = DEFAULT_WIDTH,
           height: str = DEFAULT_HEIGHT):
    """
    Resizes image file.
    Output file name is determined by input file name and out_ext.

    :param file: image file name to resize
    :param out_dir: output files directory
    :param out_ext: extension of resized image file
    :param width:  width(px) of resized image file
    :param height: height(px) of resized image file
    """
    if not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    # resize image file
    img = Image.open(file)
    img_resized = img.resize((width, height), Image.LANCZOS)
    # get basename of input file
    basename = os.path.splitext(os.path.basename(file))[0]
    # save
    out_path = os.path.join(out_dir, basename + out_ext)
    img_resized.save(out_path)


# for command line
if __name__ == '__main__':
    # get parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-file-names', nargs='*', required=True)
    parser.add_argument('--out-dir', default=DEFAULT_OUT_DIR)
    parser.add_argument('--out-extension', default=DEFAULT_OUT_EXT)
    parser.add_argument('--width', type=int, default=DEFAULT_WIDTH)
    parser.add_argument('--height', type=int, default=DEFAULT_HEIGHT)
    args = parser.parse_args()
    # ignore directories
    input_file_names = list(filter(os.path.isfile, args.input_file_names))

    print('processing...')
    resize_all(input_file_names, args.out_dir, args.out_extension, args.width, args.height,
               lambda: print('*', end='', flush=True))
    print()
    print('finished!')
