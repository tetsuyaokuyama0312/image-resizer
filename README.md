# image-resizer
This tool resizes image files.

## How to use
### 1. Install Pillow
- `pip install Pillow`

### 2. Run with GUI or CUI
#### GUI
1. `python image_resizer_gui.py`
2. Enter input file names, output directory, output extension, width, and height.
3. Press the `RESIZE START` button.

#### CUI
- `python image_resizer.py [options]`

    - Options are as follows:

        |option name|description|required|default|
        | ---- | ---- | ---- | ---- |
        |--input-file-names|image file names to resize|Y|-|
        |--out-dir|output files directory|N|./output/|
        |--out-extension|extension of resized image file|N|.png|
        |--width|width(pixel) of resized image file|N|1024|
        |--height|height(pixel) of resized image file|N|1024|

## Notes
- If directories are specified as input file names, it will not be processed for the directories.
