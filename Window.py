import tkinter
import ImageFunctions as IFun
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image

class Error(Exception):
    pass

class ImageTooSmallError(Error):
    pass

window = tkinter.Tk()

window.geometry("800x600")

def errorCallback():
    messagebox.showinfo("Error", "The selected file is not an image.", icon = "warning")

def selectImage():
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

    print("Successfully loaded image: {0}".format(path))

    try:
        emote_string = IFun.splitImage(image,"RIIIIINKO", 4)
    except IFun.TooManyPartsError:
        messagebox.showinfo("Error", "The amount of parts exceed 50.", icon = "warning")

select_file_button = tkinter.Button(window, text = "Select image...", command = selectImage)
select_file_button.place(x = 400, y = 300)

# Execute
window.mainloop()