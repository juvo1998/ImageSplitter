from PIL import Image, ImageOps

def splitImage(image, rows_cols):
    desired_rows, desired_cols = rows_cols

def trimEmptyBorders(image):
    # Only PNG has transparency
    if image.format != "PNG":
        return
        
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
    trimmed.save("test_trimmed.png", "PNG")