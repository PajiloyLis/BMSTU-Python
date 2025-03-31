from math import *
from sympy import *
from random import *
import numpy as np
LAMB = 0.4


def get_derivative(str):
    x = Symbol('x')
    derivative = diff(str, x)
    res = f"{derivative}"
    return res


def get_derivative_sign(derivative):
    return (1 if derivative > 0 else -1)


def check_is_root(value, eps):
    if value < eps:
        return True
    return False


def get_value(x, prev_x, equation, ending):
    if ending:
        return abs(eval(equation))
    else:
        y = eval(equation)
        x = prev_x
        prev_y = eval(equation)
        return abs(prev_y - y)


def get_start_point(left, right, equation):
    mean = (left+right)/2
    x = left
    l = abs(eval(equation))
    x = right
    r = abs(eval(equation))
    x = mean
    m = abs(eval(equation))
    if (l < r):
        if (l < m):
            x = left
        else:
            x = mean
    else:
        if r < m:
            x = right
        else:
            x = mean
    return x


def find_roots(equation, Nmax, left, right, eps, derivative, ending):
    x = get_start_point(left, right, equation)
    prev_x = x
    ending_flag = 1
    i = 0
    if check_is_root(get_value(x, prev_x, equation, ending), eps) and ending:
        ending_flag = 0
    else:
        for i in range(Nmax):
            prev_x = x
            try:
                x -= LAMB * \
                    get_derivative_sign(eval(derivative)) * eval(equation)
            except ZeroDivisionError:
                x -= eps*0.01
            except Exception:
                ending_flag = 2
                break
            if check_is_root(get_value(x, prev_x, equation, ending), eps):
                ending_flag = 0
                break

    if ending_flag == 0 and (x > right or x < left):
        ending_flag = 3
    return ending_flag, x, i + 1


def solve(left, right, step, Nmax, equation, eps, ending):
    roots = []
    x = left
    derivative = get_derivative(equation)
    cur_cnt = 1
    while (x < right):
        try:
            y1 = eval(equation)
        except ZeroDivisionError:
            x += 0.01*eps
            y1 = eval(equation)
            x -= 0.01*eps
        x += step
        try:
            y2 = eval(equation)
        except ZeroDivisionError:
            x += 0.01*eps
            y1 = eval(equation)
            x -= 0.01*eps
        x -= step
        if y1*y2 <= 0:
            result = find_roots(equation, Nmax, x, min(
                right, x+step), eps, derivative, ending)
            if result[0] == 0:
                tmp = x
                x = result[1]
                if (x != 0):
                    roots.append([cur_cnt, [tmp, tmp+step], x,
                                  float(eval(equation)), result[2], result[0]])
                else:
                    roots.append([cur_cnt, [tmp, tmp+step], int(x),
                                  float(eval(equation)), result[2], result[0]])
                x = tmp
            elif result[0] == 3:
                tmp = x
                x = result[1]
                roots.append([cur_cnt, [tmp, tmp+step], "",
                             "", "", result[0]])
                x = tmp
            else:
                roots.append(
                    [cur_cnt, [x, x+step], "", "", result[2], result[0]])
            cur_cnt += 1
        x += step
    return roots
