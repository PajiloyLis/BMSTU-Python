from math import modf

# Перевод в десятичную из системы с основанием base


def base_to_ten(number, base: int):
    is_neg = False
    if number[0] == '-':
        number = number[1:]
        is_neg = True
    ind = number.find(".")
    if ind == -1:
        ind = len(number)
    int_part, int_pow = 0, 1
    for i in range(ind-1, -1, -1):
        int_part += int(number[i]) * int_pow
        int_pow *= base
    float_pow, float_part = 1/base, 0
    for i in range(ind+1, len(number)):
        float_part += int(number[i]) * float_pow
        float_pow /= base
    ans = str(int_part)+"."+f"{float_part:.5g}"[2:]
    if is_neg:
        ans = '-' + ans
    return ans


# Перевод из десятичной в систему с основанием base
def ten_to_base(number, base):
    is_neg = False
    if number[0] == '-':
        number = number[1:]
        is_neg = True
    parts = tuple(number.split("."))
    int_part, float_part = int(parts[0]), 0.0
    number_of_iterations = 0
    if len(parts) == 2 and parts[1] != "":
        number_of_iterations = len(parts[1])
        float_part = int(parts[1])/10**number_of_iterations
    ans = ""
    while True:
        ans = str(int_part % base) + ans
        int_part //= base
        if int_part == 0:
            break
    ans += "."
    for i in range(number_of_iterations+5):
        if float_part.is_integer() and int(float_part) == 0:
            ans = ans+"0"
            break
        float_part *= base
        new_part, add = modf(float_part)
        ans = ans+str(int(add))
        float_part = new_part
    if is_neg:
        ans = '-' + ans
    return ans
