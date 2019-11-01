import tkinter
import ImageFunctions as IFun
from tkinter import messagebox, filedialog
from PIL import Image

class Error(Exception):
    pass

class ImageTooSmallError(Error):
    pass

class IncorrectColumnsError(Error):
    pass

window = tkinter.Tk()
window.resizable(False, False)
window.geometry("480x260")

selected_image = None

def errorCallback():
    messagebox.showinfo("Error", "The selected file is not an image.", icon = "warning")

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

    except:
        messagebox.showinfo("Error", "The selected file is not an image.", icon = "warning")
        return

    selected_image = image
    path_label.configure(text = image.filename)
    print("Successfully loaded image: {0}".format(path))

def split():
    try:
        desired_cols = int(des_col_entry.get())
        if desired_cols < 1 or desired_cols > 50:
            raise IncorrectColumnsError
        
        emote_string = IFun.splitImage(selected_image, prefix_entry.get(), desired_cols)

    except IncorrectColumnsError:
        messagebox.showinfo("Error", "The desired amount of columns should be in between 1 and 50.", icon = "warning")

    except IFun.TooManyPartsError:
        messagebox.showinfo("Error", "The amount of parts exceed 50.", icon = "warning")

    except:
        messagebox.showinfo("Error", "All fields must be completed.", icon = "warning")

# Select file button
select_file_button = tkinter.Button(window, text = "Select image...", command = selectImage)
select_file_button.place(x = 16, y = 20)

# Split execution button
split_button = tkinter.Button(window, text = "Split!", command = split)
split_button.place(x = 210, y = 200)

# Image path label
path_label = tkinter.Label(window, text = "No image selected.", wraplength = 420)
path_label.place(x = 20, y = 50)

# Prefix label
prefix_label = tkinter.Label(window, text = "Prefix:")
prefix_label.place(x = 20, y = 100)

# Prefix entry
prefix_entry = tkinter.Entry(window, width = 46)
prefix_entry.place(x = 70, y = 98)

# Desired columns label
des_col_label = tkinter.Label(window, text = "Desired number of columns:")
des_col_label.place(x = 20, y = 140)

# Desired columns entry
des_col_entry = tkinter.Entry(window, width = 3)
des_col_entry.place(x = 204, y = 138)

# Execute
window.mainloop()