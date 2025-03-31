from matplotlib import pyplot as plt
from math import *
from model import get_derivative, solve

FAILED = 0
SUCCESS = 1


def make_plot(equation, left, right, eps):
    step = (right - left)/10000
    xs, ys = [], []
    x = left
    while x <= right:
        try:
            result = eval(equation)
        except ZeroDivisionError:
            if xs < 0:
                xs -= eps/10
            else:
                xs += eps/10
        except TypeError:
            return FAILED
        except ValueError:
            print("Я вообще хз как это произошло")
            return FAILED
        except Exception:
            print("И это тоже")
            return FAILED
        else:
            xs.append(x)
            ys.append(result)
            # if x > left+step and (ys[-2]-ys[-3])*(ys[-2]-ys[-1]) > 0:
            #     points.append(x)
            #     values.append(result)
            x += step
    fig1, = plt.plot(xs, ys, label="plot")
    diff = get_derivative(equation)
    solutions = solve(left, right, step, 10, diff, 0.01, 1)
    points = []
    for i in range(len(solutions)):
        if not solutions[i][5]:
            x = float(solutions[i][2])
            if eval(get_derivative(diff)):
                points.append(float(solutions[i][2]))
    values = []
    for x in points:
        values.append(float(eval(equation)))
    fig2, = plt.plot(points, values, "or", linewidth=4, label="extremes")
    handles=[fig1, fig2]
    plt.grid(visible=True)
    return SUCCESS, handles


def append_roots(roots, equation, handles):
    points = []
    for i in range(len(roots)):
        if not roots[i][5]:
            points.append(float(roots[i][2]))
    values = []
    for x in range(len(points)):
        values.append(0)
    fig3, = plt.plot(points, values, "og", linewidth=4, label="roots")
    handles.append(fig3)
    plt.legend(handles = handles)
    plt.savefig("plt.jpg")
    plt.close()
