import math
from cProfile import label
from math import log, exp

import sympy
from sympy import solve_linear_system, Number
from sympy import Eq

from metrix import *

import matplotlib.pyplot as plt
import numpy as np

n = 0
X = []
Y = []

x = sympy.Symbol("x")


def _s(powX=1, powY=0, x_arr=X, y_arr=Y) -> float:
    return sum(pow(x, powX) * pow(y, powY) for x, y in zip(x_arr, y_arr))


def s(option, x_arr=X, y_arr=Y) -> float:
    return _s(option.count("x"), option.count("y"), x_arr=x_arr, y_arr=y_arr)

def linear_with_coefs(x_arr, y_arr):
    sx = s("x", x_arr=x_arr, y_arr=y_arr)
    sxx = s("xx", x_arr=x_arr, y_arr=y_arr)
    sy = s("y", x_arr=x_arr, y_arr=y_arr)
    sxy = s("xy", x_arr=x_arr, y_arr=y_arr)

    a, b = sympy.symbols("a b")

    solution = sympy.solve((
        Eq(a * sxx + b * sx, sxy),
        Eq(a * sx + b * n, sy)
    ), (a, b))

    a = solution[a].evalf()
    b = solution[b].evalf()

    return a * x + b, a, b

def linear(x_arr=X, y_arr=Y):
    f, a, b = linear_with_coefs(X, Y)
    return f, {"a": a, "b": b}, f"{b} + {a}x"


def square():
    sx = s("x")
    sxx = s("xx")
    sxxx = s("xxx")
    sxxxx = s("xxxx")

    sy = s("y")
    sxy = s("xy")
    sxxy = s("xxy")

    a, b, c = sympy.symbols("a b c")

    solutions = sympy.solve((
        Eq(n * a + sx * b + sxx * c, sy),
        Eq(sx * a + sxx * b + sxxx * c, sxy),
        Eq(sxx * a + sxxx * b + sxxxx * c, sxxy)),
        (a, b, c)
    )
    a, b, c = solutions[a].evalf(), solutions[b].evalf(), solutions[c].evalf()

    return a + b * x + c * (x ** 2), {"a": a, "b": b, "c" : c}, f"{a} + {b}x + {c}x^2"


def cube():
    sx = s("x")
    sxx = s("xx")
    sxxx = s("xxx")
    sxxxx = s("xxxx")
    sxxxxx = s("xxxxx")
    sxxxxxx = s("xxxxxx")

    sy = s("y")
    sxy = s("xy")
    sxxy = s("xxy")
    sxxxy = s("xxxy")

    a, b, c, d = sympy.symbols("a b c d")
    solutions = sympy.solve((
        Eq(n * a + sx * b + sxx * c + sxxx * d, sy),
        Eq(sx * a + sxx * b + sxxx * c + sxxxx * d, sxy),
        Eq(sxx * a + sxxx * b + sxxxx * c + sxxxx * d, sxxy),
        Eq(sxxx * a + sxxxx * b + sxxxxx * c + sxxxxxx * d, sxxxy)),
        (a, b, c, d)
    )
    a, b, c, d = solutions[a].evalf(), solutions[b].evalf(), solutions[c].evalf(), solutions[d].evalf()

    return a + b * x + c * x ** 2 + d * x ** 3, {"a": a, "b": b, "c" : c, "d": d}, f"{a} + {b}x + {c}x^2 + {d}x^3"


def exponential():
    _X = list(map(log, X))
    _, a, b = linear_with_coefs(x_arr=_X, y_arr=Y)

    a = exp(a)
    b = b

    return a * (sympy.exp(b * x)), {"a": a, "b": b}, f"{a} * e^{b}x"


def logarithmic():
    _Y = list(map(log, Y))
    _, a, b = linear_with_coefs(x_arr=X, y_arr=_Y)

    return a + b * sympy.log(x), {"a": a, "b": b}, f"{a} + {b} * ln(x)"


def power():
    xs = list(map(math.log, X))
    ys = list(map(math.log, Y))
    _, a, b = linear_with_coefs(x_arr=xs, y_arr=ys)

    if (abs(b) < 1e-10):
        b = 0
    b = exp(b)

    return b * (x ** a), {"a": a, "b": b}, f"{b} * x^{a}"


def round_expr(expr, num_digits=3):
    return expr


def get_det_word(val):
    if val > 0.95:
        return "высокая"
    if 0.75 < val < 0.95:
        return "удовлетворительная"
    if 0.5 < val < 0.75:
        return "слабая"
    return "недостаточная"

def dict_to_string(d: dict) -> str:
    result = ""
    for key, value in d.items():
        result += f"{key}={round(value, 3)} "
    return result

def read_from_cli():
    try:
        n = int(input("Введите количество точек: "))

        # if not (8 <= n <= 12):
        #     raise TypeError("Неверное количество точек")

        for i in range(n):
            x_i, y_i = map(float, input(f"{i + 1}:").strip().split(" "))
            X.append(x_i)
            Y.append(y_i)
    except Exception as e:
        raise TypeError("Некорректный ввод")


def read_from_file(filename:str):
    try:
        with open(filename, "r") as file:
            n = int(file.readline())
            for i in range(n):
                x_i, y_i = map(float, file.readline().strip().split(" "))
                X.append(x_i)
                Y.append(y_i)
        print("Файл прочитан")
    except:
        raise TypeError(f"Не получилось прочитать файл {filename}")




def main():
    input_type = input("Выберите тип ввода: к - консоль, ф - файл: ")
    if input_type == "к":
        read_from_cli()
    elif input_type == "ф":
        filename = input("Введите файл: ")
        read_from_file(filename)
    functions = [
        (linear, "Линейная"),
        (square, "Полиноминальная 2-й степени"),
        (cube, "Полиноминальная 3-й степени")
    ]
    if all(map(lambda xi: xi > 0, X)):
        if all(map(lambda yi: yi > 0, Y)):
            functions.append((exponential, "Экспоненциальная"))
            functions.append((logarithmic, "Логарифмическая"))
            functions.append((power, "Степенная"))
        else:
            functions.append((logarithmic, "Логарифмическая"))
    else:
        if all(map(lambda yi: yi > 0, Y)):
            functions.append((exponential, "Экспоненциальная"))

    linspace = np.linspace(min(X) - 0.5, max(X) + 0.5)

    best = None
    best_name = None
    best_R = -1

    plt.scatter(X, Y, label="Вводные точки")


    for func, name in functions:
        approximation, coeffs, fun_str = func()
        rounded = round_expr(approximation)

        det = determination_coef(approximation, x, X, Y)

        if det > best_R:
            best_R = det
            best = [approximation]
            best_name = [name]
        elif det == best_R or (abs(det - best_R) < 1e-10):
            best_name.append(name)
            best.append(approximation)

        lambdified = sympy.lambdify(x, approximation)

        plt.plot(linspace, lambdified(linspace), label=name)

        print("-"*40)

        print(f"{name}:{rounded}")
        print(f"Функция: {fun_str}")
        print(f"Коэфиценты: {dict_to_string(coeffs)}")

        print(f"СКО: {mean_square_deviation(approximation, x, X, Y)}")
        print(f"Коэф. детерминации: {det} => {get_det_word(det)} точность аппроксимации")

        if (name == "Линейная"):
            print(f"Коэффицент Пирсона: {correlation(X, Y)}")
    plt.legend()
    plt.title("Все функции")
    plt.show()

    print("-"*40)
    print(f"Найдено наилучших функций: {len(best)}")
    print(f"Наибольший коэффицент детерминации: {best_R}")
    for best_f_i, best_name_i in zip(best, best_name):
        print(f"{best_name_i}: {best_f_i}")
        best_lambdified = sympy.lambdify(x, best_f_i)
        plt.plot(linspace, best_lambdified(linspace), label=best_name_i)
        print("-" * 40)

    plt.title("Наилучшие функции")
    plt.scatter(X, Y, label="Введенные точки")

    plt.legend()
    plt.show()

try:
    main()
except TypeError as e:
    print(e)
