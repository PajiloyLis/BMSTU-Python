from PIL import Image
import numpy as np
CHAR_LEN = 8
COLORS_COUNT = 3
PIX_FOR_CHAR = 3
EXIT_SUCCESS = 0
EXIT_OVERFLOW = 1
EXIT_PERMISSON = 2
EXIT_OTHER = 3

# Кодирование
def code(cur_file, string, new_file):

    # Открытие файла
    try:
        image = Image.open(cur_file)
    except PermissionError:
        return EXIT_PERMISSON, "Доступ отклонен"
    except Exception:
        return EXIT_OTHER, "Непредвиденная ошибка открытия файла"

    # Проверка размеров и получение массива картинки
    height, width = image.size[1], image.size[0]
    string = str(len(string))+" "+string
    if (height*width//3 < len(string)):
        return EXIT_OVERFLOW, "Размер текста превышает размер"
    image_array = np.array(image)
    scalar_image_array = np.reshape(
        image_array, width*height*COLORS_COUNT)

    # Шифрование
    for i in range(len(string)):
        for bit in range(CHAR_LEN-1, -1, -1):
            cur_char_bit = ((ord(string[i]) >> bit) & 1)
            scalar_image_array[i*COLORS_COUNT *
                               PIX_FOR_CHAR+CHAR_LEN-1-bit] >>= 1
            scalar_image_array[i*COLORS_COUNT *
                               PIX_FOR_CHAR+CHAR_LEN-1-bit] <<= 1
            scalar_image_array[i*COLORS_COUNT *
                               PIX_FOR_CHAR+CHAR_LEN-1-bit] += cur_char_bit
    new_image_array = np.reshape(
        scalar_image_array, (height, width, COLORS_COUNT))

    # Сохранение картинки
    try:
        Image.fromarray(new_image_array).save(new_file)
    except PermissionError:
        return EXIT_PERMISSON, "Доступ отклонен"
    except Exception:
        return EXIT_OTHER, "Непредвиденная ошибка открытия файла"
    return EXIT_SUCCESS, None


# Декордировка
def decode(cur_file):

    # Открытие картинки
    try:
        image = Image.open(cur_file)
    except PermissionError:
        return EXIT_PERMISSON, None
    except Exception:
        return EXIT_OTHER, None
    
    # Получение размера файла
    _ = np.array(image)
    image_array = np.reshape(_, image.size[0]*image.size[1]*COLORS_COUNT)
    ch, count, cur_ind = 0, 0, 0
    while chr(ch) != ' ':
        if ch != 0:
            try:
                count = count*10+int(chr(ch))
            except ValueError:
                return EXIT_OTHER, None
            ch = 0
        for i in range(CHAR_LEN-1, -1, -1):
            ch += ((image_array[cur_ind] & 1) << i)
            cur_ind += 1
        cur_ind += 1
    
    # Декодировка непосредственно строки
    string = ""
    for i in range(count):
        ch = 0
        for j in range(CHAR_LEN-1, -1, -1):
            ch += ((image_array[cur_ind] & 1) << j)
            cur_ind += 1
        cur_ind += 1
        string += chr(ch)
    return EXIT_SUCCESS, string
