from math import exp

import numpy as np
import matplotlib.pyplot as plt

from methods import adams, improved_euler_method, fourth_order_runge_kutta_method

functions = [
    {
        "name": "y' = y + (1 + x)*y^2",
        "func": lambda x, y: y + (1 + x) * y ** 2,
        "exact_f": lambda x, x0, y0: -exp(x) / (x*exp(x) - (x0*exp(x0)*y0 + exp(x0)) / y0)
    },
    {
        "name": "y' = sin(x) - y",
        "func": lambda x, y: np.sin(x) - y,
        "exact_f": lambda x, x0, y0: (np.sin(x) - np.cos(x) + np.exp(-x))/2
    },
    {
        "name": "y' = y / x",
        "func": lambda x, y: y / x,
        "exact_f": lambda x, x0, y0: (x * y0) / x0
    }
]

def split(x_0, x_n, h):
    xs = []

    while x_0 <= x_n:
        xs.append(x_0)
        x_0 += h

    if abs(xs[-1] - x_n) < 1e-10:
        return xs
    xs.append(x_n)

    return xs

def find_dot(origin, current):
    for or_val in origin:
        if abs(or_val - current) < 1e-10:
            return True
    return False

MAX_ITERATIONS = 10
ITERATIONS_CHANGE = 10

def one_step(f, x0, xn, h, y0, epsilon, method, p):
    MAX_ITERATIONS = 10

    iter = 0

    error = np.inf

    xs = split(x0, xn, h)
    ys = method(f, xs, y0)

    while error > epsilon:
        print(f"Вычисляю {iter+1} итерацию......")

        if (iter >= MAX_ITERATIONS):
            to_continue = input(f"Алгоритм выполнил {iter+1} итераций и не достиг желаемой точности, продолжать?: ")
            if to_continue.strip() == "да":
                MAX_ITERATIONS +=  ITERATIONS_CHANGE
            else:
                break

        h = h / 2
        xs = split(x0, xn, h)
        ys_new = method(f, xs, y0)

        error = abs(ys_new[-1] - ys[-1]) / (2**p - 1)

        print(f"h = {h * 2}, последний y = {ys[-1]}")
        print(f"h = {h}, последний y = {ys_new[-1]}")

        ys = ys_new.copy()


        iter += 1



    print(f"Алгоритм выполнил {iter} итераций")
    print(f"Правило Рунге было достигнуто при h={h}")

    return xs, ys

def many_step(f, f_exact, x0, xn, h, y0, epsilon):
    MAX_ITERATIONS = 10
    iter = 0

    f_exact_m = lambda x: f_exact(x, x0, y0)
    xs = split(x0, xn, h)
    y_real = list(map(f_exact_m, xs))
    ys = adams(f, xs, y0, epsilon)
    error = max([abs(y_real_i - ys_i) for y_real_i, ys_i in zip(y_real, ys)])

    while error > epsilon:
        if (iter >= MAX_ITERATIONS):
            to_continue = input(f"Алгоритм выполнил {iter+1} итераций и не достиг желаемой точности, продолжать: ")
            if to_continue.strip() == "да":
                MAX_ITERATIONS += ITERATIONS_CHANGE
            else:
                break
        iter += 1

        h /= 2
        xs = split(x0, xn, h)

        y_real = list(map(f_exact_m, xs))
        ys = adams(f, xs, y0, epsilon)
        error = max([abs(y_real_i - ys_i) for y_real_i, ys_i in zip(y_real, ys)])

    print(f"Алгоритм выполнил {iter +1} итерацию")
    print(f"Правило Рунге было достигнуто при h={h}")

    return xs, ys

def main():
    print("Выберите функцию")
    for ind, value in enumerate(functions):
        print(f"{ind+1}: {value['name']}")
    f_ind = int(input("Введите номер функции: ")) - 1

    print("Задайте начальные условия:")
    x0, xn = map(float, input("Введите интервал: ").strip().split())
    h = float(input("Введите шаг: "))
    xs_original = split(x0, xn, h)
    y0 = float(input("Введите y0: "))
    epsilon = float(input("Введите точность: "))
    only_key_point = input("Выводить только узловые точки?: ").strip() == "да"

    print("Выберите метод:")
    print(
            "1. Усовершенствованный метод Эйлера",
            "2. Метод Рунге-Кутта 4-го порядка",
            "3. Метод Адамса", sep="\n"
    )
    f, f_exact = functions[f_ind]["func"], functions[f_ind]["exact_f"]

    method_ind = int(input("Введите номер метода: "))
    if method_ind == 1:
        xs, ys = one_step(f, x0, xn, h, y0,  epsilon, improved_euler_method, 2)
    elif method_ind == 2:
        xs, ys= one_step(f, x0, xn, h, y0,  epsilon, fourth_order_runge_kutta_method,4)
    else:
        xs, ys= many_step(f, f_exact, x0, xn, h, y0, epsilon)

    n = len(xs)

    exact = []
    print("i", "x_i", "y_i", "y_точн", sep="\t")
    for i in range(n):
        real = f_exact(xs[i], x0, y0)
        exact.append(real)
        if only_key_point and not find_dot(xs_original, xs[i]):
            continue
        print(f"{i:4}:\t {xs[i]:.8f}\t {ys[i]:.8f}\t {real:.8f}")



    plt.xlabel("X")
    plt.ylabel("Y")
    plt.scatter(xs, ys, c='r', label="Найденные приближения")
    plt.plot(xs, exact, color="b", label="Точные значения")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    try:
        main()
    except OverflowError:
        print("Число слишком большое, мне могу такое вычислить")




