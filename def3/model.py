from PIL import Image
import numpy as np
COLOR_COUNTS = 3


def binarize(file_name, bound, new_file):
    image = Image.open(file_name)
    image_array = np.array(image)

    height, width = image.size[1], image.size[0]
    for i in range(height):
        for j in range(width):
            for k in range(COLOR_COUNTS):
                image_array[i][j][k] = 0 if image_array[i][j][k] < bound else 255

    Image.fromarray(image_array).save(new_file)

