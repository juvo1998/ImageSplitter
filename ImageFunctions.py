import math
from PIL import Image, ImageOps

class Error(Exception):
    pass

class TooManyPartsError(Error):
    pass

class TooManyRowsError(Error):
    pass

def splitImage(image, prefix, desired_cols):
    # We are only given desired_cols, as we will calculate the desired_rows based on the aspect ratio.
    image = trimEmptyBorders(image)
    im_width, im_height = image.size
    print("Image has width = {0}, and height = {1}".format(im_width, im_height))
    part_width = int(im_width // desired_cols)
    print("Each part has width = {0}".format(part_width))
    new_im_width = part_width * desired_cols
    print("The new im_width = {0}".format(new_im_width))
    reduce_ratio = im_width / new_im_width
    new_im_height = round(im_height / reduce_ratio)
    print("The new im_height = {0}".format(new_im_height))
    desired_rows = math.ceil(new_im_height / part_width)
    newer_im_height = part_width * desired_rows
    print("The even newer im_height = {0}".format(newer_im_height))

    # Because Discord only allows 50 emotes per server, limit parts <= 50
    if desired_cols * desired_rows > 50:
        raise TooManyPartsError

    image = image.resize((new_im_width, new_im_height))
    new_size = (new_im_width, newer_im_height)
    blank = (0, 0, 0, 0)
    new_canvas = Image.new("RGBA", new_size, blank)
    new_canvas.paste(image)

    emote_string = ""

    # Begin the crops / splits
    for y in range(desired_rows):
        for x in range(desired_cols):
            left = x * part_width
            top = y * part_width
            right = left + part_width
            bot = top + part_width

            part = new_canvas.crop((left, top, right, bot))
            
            if y == 0:
                suffix_row = "A"
            elif y == 1:
                suffix_row = "B"
            elif y == 2:
                suffix_row = "C"
            elif y == 3:
                suffix_row = "D"
            elif y == 4:
                suffix_row = "E"
            elif y == 5:
                suffix_row = "F"
            elif y == 6:
                suffix_row = "G"
            elif y == 7:
                suffix_row = "H"
            elif y == 8:
                suffix_row = "I"
            elif y == 9:
                suffix_row = "J"
            elif y == 10:
                suffix_row = "K"
            elif y == 11:
                suffix_row = "L"
            else:
                raise TooManyRowsError

            suffix_col = str(x + 1)
            emote_string += ":{0}_{1}{2}:".format(prefix, suffix_row, suffix_col)
            part.save("{0}_{1}{2}.png".format(prefix, suffix_row, suffix_col), "PNG")
        
        emote_string += "\n"
    
    print(emote_string.strip())
    return emote_string.strip()

def trimEmptyBorders(image):
    image = image.convert("RGBA")
    width, height = image.size
    desired_left_x = 0
    desired_right_x = width - 1
    desired_top_y = 0
    desired_bot_y = height - 1

    found_top = False
    found_left = False

    # Iterate through (horizontally). Keep track of transparent rows, and denote the desired y-value.
    # For the top rows: the moment we hit a non-transparent pixel, we can call that row the desired_y.
    for y in range(height):
        for x in range(width):
            _, _, _, alpha = image.getpixel((x, y))
            if alpha != 0:
                if not found_top:
                    desired_top_y = y
                    found_top = True
                desired_bot_y = y
                break

    for x in range(width):
        for y in range(height):
            _, _, _, alpha = image.getpixel((x, y))
            if alpha != 0:
                if not found_left:
                    desired_left_x = x
                    found_left = True
                desired_right_x = x
                break

    trimmed = image.crop((desired_left_x, desired_top_y, desired_right_x + 1, desired_bot_y + 1))
    return trimmed

def splitGif(gif, prefix, desired_cols):
    # print(gif.n_frames)
    # gif.seek(gif.n_frames - 1)
    # gif.save("last_frame.png", "PNG")
    images = []
    # reverse for testing
    num_frames = gif.n_frames
    for n in range(num_frames - 1, -1, 1):
        gif.seek(n)
        frame = gif.copy()
        frame.convert("RGBA")
        images.append(frame)
    
    images.save("out_gif", save_all = True, append_images = images)
