"""
GUI of image-resizer.
"""
import os
import itertools
import tkinter as tk
import tkinter.filedialog as fd

import image_resizer
import async_util

POS_X = 10
INPUT_FILE_TYPES = [
    ('image file', '*.bmp;*.jpeg;*.jpg;*.png;*.ppm;*.gif;*.tiff')
]


def on_select_files_button_click():
    in_files = infile_text.get(1.0, 'end -1c')

    def get_ini_dir(in_paths: str):
        head_path = in_paths.split()[0]
        return os.path.basename(head_path) if os.path.isdir(head_path) else os.path.dirname(head_path)

    ini_dir = get_ini_dir(in_files) if in_files else os.path.abspath(os.path.dirname(__file__))
    file_names = fd.askopenfilenames(filetypes=INPUT_FILE_TYPES,
                                     initialdir=ini_dir)
    if file_names:
        if in_files:
            infile_text.insert('end', ' ')
        infile_text.insert('end', file_names)


def on_clear_files_button_click():
    infile_text.delete(1.0, 'end')


def on_select_dir_button_click():
    out_dir = out_dir_text.get(1.0, 'end -1c')
    if not os.path.exists(out_dir):
        out_dir = os.path.abspath(os.path.dirname(__file__))

    dir_name = fd.askdirectory(initialdir=out_dir)
    if dir_name:
        out_dir_text.delete(1.0, 'end')
        out_dir_text.insert(1.0, dir_name)


def on_resize_start_button_click():
    # get parameters
    input_files_text = infile_text.get(1.0, 'end -1c')
    # ignore directories
    input_files = list(filter(os.path.isfile, input_files_text.split())) if input_files_text else None
    if not input_files:
        status.set('Could not get input files')
        return
    optional_params = get_optional_params()

    # define callback
    total = len(input_files)
    counter = itertools.count()

    def callback():
        update_progress(total, next(counter))

    # call callback once to initialize progress
    callback()
    # resize
    async_util.submit(lambda: image_resizer.resize_all(input_files, **optional_params,
                                                       callback=callback))


def get_optional_params():
    optional_params = {}
    out_dir = out_dir_text.get(1.0, 'end -1c')
    if out_dir:
        optional_params['out_dir'] = out_dir

    out_ext = out_ext_text.get(1.0, 'end -1c')
    if out_ext:
        optional_params['out_ext'] = out_ext

    width = width_text.get(1.0, 'end -1c')
    if width:
        optional_params['width'] = int(width)

    height = height_text.get(1.0, 'end -1c')
    if height:
        optional_params['height'] = int(height)
    return optional_params


def update_progress(total: int, completed: int):
    status.set(f'{completed} / {total} completed')


root = tk.Tk()
root.title('image-resizer')
root.geometry('500x440+0+0')

infile_label = tk.Label(text='input file names')
infile_label.place(x=POS_X, y=10)
infile_text = tk.Text(width=50)
infile_text.place(x=POS_X, y=30, height=50)
infile_button = tk.Button(root, text='select files', width=15, height=30, command=on_select_files_button_click)
infile_button.place(x=POS_X + 365, y=30, height=20)
infile_clear_button = tk.Button(root, text='clear files', width=15, height=30, command=on_clear_files_button_click)
infile_clear_button.place(x=POS_X + 365, y=60, height=20)

out_dir_label = tk.Label(text='output directory (default = ./output/)')
out_dir_label.place(x=POS_X, y=90)
out_dir_text = tk.Text(width=50)
out_dir_text.insert(1.0, os.path.join(os.path.abspath(os.path.dirname(__file__)), 'output'))
out_dir_text.place(x=POS_X, y=110, height=50)
out_dir_button = tk.Button(root, text='select directory', width=15, height=30, command=on_select_dir_button_click)
out_dir_button.place(x=POS_X + 365, y=110, height=20)

out_ext_label = tk.Label(text='output file extension (default = .png)')
out_ext_label.place(x=POS_X, y=170)
out_ext_text = tk.Text(width=10)
out_ext_text.insert(1.0, '.png')
out_ext_text.place(x=POS_X, y=190, height=20)

width_label = tk.Label(text='width(px) (default = 1024)')
width_label.place(x=POS_X, y=220)
width_text = tk.Text(width=10)
width_text.insert(1.0, '1024')
width_text.place(x=POS_X, y=240, height=20)

height_label = tk.Label(text='height(px) (default = 1024)')
height_label.place(x=POS_X, y=270)
height_text = tk.Text(width=10)
height_text.insert(1.0, '1024')
height_text.place(x=POS_X, y=300, height=20)

resize_start_button = tk.Button(root, text='RESIZE START', width=50, height=3, command=on_resize_start_button_click)
resize_start_button.place(x=POS_X, y=340)

status = tk.StringVar()
status_label = tk.Label(root, textvariable=status)
status_label.place(x=POS_X, y=400)

root.mainloop()
