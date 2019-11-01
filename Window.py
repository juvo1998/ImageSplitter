import tkinter
import ImageFunctions as IFun
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image

window = tkinter.Tk()

window.geometry("800x600")

def errorCallback():
    messagebox.showinfo("Error", "The selected file is not an image.", icon = "warning")

def selectImage():
    path = filedialog.askopenfilename(parent = window)
    try:
        image = Image.open(path)
    except:
        messagebox.showinfo("Error", "The selected file is not an image.", icon = "warning")
        return

    print("Successfully loaded image: {0}".format(path))
    IFun.trimEmptyBorders(image)

select_file_button = tkinter.Button(window, text = "Select image...", command = selectImage)
select_file_button.place(x = 400, y = 300)

# Execute
window.mainloop()