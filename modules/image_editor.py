import simpleimage

# Function to apply transformations and return a list of transformed images
def get_transforms(file1: str, file2: str) -> list:

    # Placeholder lists for all transformed images
    ls = []
    image1 = simpleimage.Image(file1)
    image2 = simpleimage.Image(file2)

    # Shrink both images
    image1 = image1.shrink(5)

    image2 = image2.shrink(5)
    ls.append(image1)

    # Append images with effects to ls
    ls.append(image1.grayscale())

    ls.append(image1.sepia())

    ls.append(image1.blur())

    ls.append(image1.filter("red", 100))

    ls.append(image1.filter("green", 100))

    ls.append(image1.filter("blue", 100))

    ls.append(image1.flip(0))

    ls.append(image1.flip(1))

    ls.append(image1.greenscreen("red", 100, image2))

    ls.append(image1.greenscreen("green", 100, image2))

    ls.append(image1.greenscreen("blue", 100, image2))

    return ls

# Function to compose the final 5x5 grid of images
def compose(img_list: list) -> simpleimage:

    # Get dimensions of each image - only first needed because all dimensions should be the same
    image1 = img_list[0]
    height = image1.height
    width = image1.width

    # Offsets - currently at 0
    dx = 0
    dy = 0

    # Canvas must be 5 times the size both ways
    canvas = simpleimage.blank(image1.width * 5, image1.height * 5)

    # Loop to repeat image pasting
    while True:
        # Select random image
        toset = img_list[random.randint(0, 11)]

        # Looping through the column
        for y in range(canvas.height):
            # Checks if y is within height of image to be pasted WITH the offset
            if dy <= y < height + dy:
                # Looping through the rows
                for x in range(canvas.width):
                    # Checks if x is within width of image to be pasted WITH the offset
                    if dx <= x < width + dx:
                        # Set pixel
                        canvas.set_pixel(x, y, toset.get_pixel(x - dx, y - dy))

        # If y isn't within the pasted image dimensions -> add to the offset by one image height
        dy += height

        # If height goes beyond canvas dimensions -> move window to the right by one image and update y-offset to 0
        if height + dy > canvas.height:
            dx += width
            dy = 0

        # If height and width of canvas are filled -> break loop
        if width + dx > canvas.width:
            break

    # Write to "pop.jpg"
    canvas.write("pop.jpg")

    return canvas