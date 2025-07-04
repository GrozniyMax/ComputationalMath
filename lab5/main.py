import math

import matplotlib.pyplot as plt
import numpy as np

from solvers import functions, print_finite_differences_table, calculate_finite_differences


def read_from_file():
    filename = input("Введите имя файла: ").strip()
    with open(filename, 'r') as f:
        x_inter = float(f.readline().strip())
        xs = []
        ys = []
        for line in f:
            x, y = map(float, line.strip().split(" "))
            xs.append(x)
            ys.append(y)
        return x_inter, xs, ys

def read_from_table():
    x_inter = float(input("Введите точку интерполяции: "))
    print("Вводите точки, потом вводите команду quit(q)")
    count = 0
    xs = []
    ys = []
    while True:
        line = input("# ")
        if line == "quit" or line == "q":
            break
        x, y = map(float, line.strip().split(" "))
        xs.append(x)
        ys.append(y)
    return x_inter, xs, ys

def read_from_funtion():
    print("1: x² - x + 12")
    print("2: x⁵")
    print("3: sin(x)")

    func_index = int(input("Введите индекс выбранной функции: "))
    f = None
    if func_index == 1:
        f = lambda x: x**2 - x + 12
    elif func_index == 2:
        f = lambda x: x**5
    elif func_index == 3:
        f = lambda x: math.sin(x)
    else:
        raise TypeError("Такой функции не существует")

    x_inter = float(input("Введите точку интерполяции: "))
    xs = list(map(float, input("Введите значения x: ").split(" ")))

    ys = list(map(f, xs))

    return x_inter, xs, ys

def read_input():
    print("Выберите тип ввода(1-файл, 2-таблица, 3-функция)")
    type = int(input("# "))
    f = None
    if type == 1:
        f = read_from_file
    elif type == 2:
        f = read_from_table
    elif type == 3:
        f = read_from_funtion
    else:
        raise TypeError("Такого типа ввода я не знаю")


    return f()

def check_difference(X):
    if len(X) < 3:
        raise TypeError("Точек слишком мало")
    expected_diff = X[1] - X[0]

    if expected_diff <= 0:
        raise TypeError("Точки должны быть в порядке возрастания")

    for i in range(2, len(X)):
        current_diff = X[i] - X[i-1]
        if current_diff <= 0:
            raise TypeError("Точки должны быть в порядке возрастания")
        if abs(expected_diff - current_diff) > 1e-5:
            print("! У вас неравноотстоящие узлы. Поэтому метод Ньютона с конечными разностями применить не получится ")
            return False
    return True

def check(x_inter, xs):
    x_min = min(xs)
    x_max = max(xs)
    middle = (x_max - x_min)/2

    if x_inter < middle:
        return True
    return False

def main():

    x_inter, xs, ys = read_input()
    n = len(xs)
    print_finite_differences_table(calculate_finite_differences(ys))

    linspace = np.linspace(xs[0], xs[-1], int((xs[-1] - xs[0])/0.001))

    equal_diffs = check_difference(xs)

    first_part = check(x_inter, xs)

    print("Значения функции")
    for name, func in functions.items():
        if "Формула" in name and not equal_diffs:
            continue
        if "Формула" not in name and equal_diffs:
            continue

        if "2" in name and first_part:
            continue

        if "1" in name and not first_part:
            continue

        value = func(x_inter, xs ,ys, n)
        plt.scatter(xs, ys, color='b')
        plt.scatter(x_inter, value, color='r')
        plt.plot(linspace, func(linspace, xs, ys, n), color='g')
        print(f"{name}: {func(x_inter, xs ,ys, n):.4f}")
        plt.title(name)
        plt.show()

try:
    main()
except TypeError as e:
    print(e)
except Exception as e:
    print("Unexpected error", e)