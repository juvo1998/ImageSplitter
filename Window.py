import tkinter
import sys
import os
import ImageFunctions as IFun
from tkinter import messagebox, filedialog, ttk
from PIL import Image

class Error(Exception):
    pass

class ImageTooSmallError(Error):
    pass

class IncorrectColumnsError(Error):
    pass

window = tkinter.Tk()
window.title("ImageSplitter")

try:
    wd = sys._MEIPASS
except:
    wd = "."
yg = os.path.join(wd, "YuiGoggles.ico")
if "nt" == os.name:
    window.wm_iconbitmap(bitmap = yg)

window.resizable(False, False)
window.geometry("500x420")

selected_image = None

def selectImage():
    global selected_image
    path = filedialog.askopenfilename(parent = window)
    try:
        image = Image.open(path)
        width, height = image.size
        if width < 50 and height < 50:
            raise ImageTooSmallError

    except ImageTooSmallError:
        messagebox.showinfo("Error", "The image selected is too small.", icon = "warning")

    except AttributeError:
        # User clicked cancel
        return

    except:
        messagebox.showinfo("Error", "The selected file is not an image, or the image type is not supported.", icon = "warning")
        return

    selected_image = image
    path_label.configure(text = image.filename)
    print("Successfully loaded image: {0}".format(path))

def split():
    try:
        desired_cols = int(des_col_entry.get())
        if desired_cols < 1 or desired_cols > 50:
            raise IncorrectColumnsError
        
        # IFun.reverseGif(selected_image, prefix_entry.get(), desired_cols)
        emote_string = IFun.splitGif(selected_image, prefix_entry.get(), desired_cols)
        # emote_string = IFun.splitImage(selected_image, prefix_entry.get(), desired_cols)
        # window.clipboard_clear()
        # window.clipboard_append(emote_string)
        # window.update()

    except IncorrectColumnsError:
        messagebox.showinfo("Error", "The desired amount of columns should be in between 1 and 50.", icon = "warning")

    except IFun.TooManyPartsError:
        messagebox.showinfo("Error", "The amount of parts exceed 50.", icon = "warning")

    except IFun.TooManyRowsError:
        messagebox.showinfo("Error", "There are too many rows given the desired columns.", icon = "warning")

    # except:
    #     messagebox.showinfo("Error", "All fields must be completed.", icon = "warning")

# File frame
file_frame = tkinter.Frame(window)
file_frame.pack(pady = (20, 10))

# Select file button
select_file_button = tkinter.Button(file_frame, text = "Select image...", command = selectImage)
select_file_button.pack(side = "left")

# Image path label
path_label = tkinter.Label(file_frame, text = "No image selected.", wraplength = 420)
path_label.pack(side = "left")

# Prefix frame
prefix_frame = tkinter.Frame(window)
prefix_frame.pack(pady = 10)

# Prefix label
prefix_label = tkinter.Label(prefix_frame, text = "Prefix:")
prefix_label.pack(side = "left")

# Prefix entry
prefix_entry = tkinter.Entry(prefix_frame, width = 46)
prefix_entry.pack(side = "left")

# Desired columns frame
des_col_frame = tkinter.Frame(window)
des_col_frame.pack(pady = 10)

# Desired columns label
des_col_label = tkinter.Label(des_col_frame, text = "Desired number of columns:")
des_col_label.pack(side = "left")

# Desired columns entry
des_col_entry = tkinter.Entry(des_col_frame, width = 3)
des_col_entry.pack(side = "left")

# Split execution button
split_button = tkinter.Button(window, text = "Split!", command = split, height = 2, width = 10)
split_button.pack(side = "bottom", pady = 10)

# Copy label
copy_label = tkinter.Label(window, text = "Note: your clipboard will have the full emote string after splitting.")
copy_label.pack(side = "bottom")

# Progress bar
progress = ttk.Progressbar(window, length = 300)
progress.pack(side = "bottom", pady = 10)

# Execute
window.mainloop()