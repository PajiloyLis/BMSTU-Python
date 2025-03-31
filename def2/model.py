from math import *


def calc_f(x):
    return sin(x)


def calc_derivative(x):
    return cos(x)


def calc(a, b, eps):
    medium = (a+b)/2
    sin_a, sin_b, sin_m = abs(sin(a)), abs(sin(b)), abs(sin(medium))
    if sin_a < sin_b:
        if sin_a < sin_m:
            x = a
        else:
            x = medium
    else:
        if sin_b < sin_m:
            x = b
        else:
            x = medium
    while (cur_sin := calc_f(x)) >= eps:
        x -= cur_sin/calc_derivative(x)
    return x
