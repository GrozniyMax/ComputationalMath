from math import factorial

# Норм
def lagrange(x, xs, ys, n):
    s = 0
    for i in range(n):
        prod = 1
        for j in range(n):
            if i == j:
                continue
            prod *= (x - xs[j]) / (xs[i] - xs[j])
        s += ys[i] * prod
    return s

#Норм
def calculate_divided_differences(x, y):
    n = len(y)
    coefs = y.copy()
    for j in range(1, n):
        prod = 1.0
        for i in range(n - 1, j - 1, -1):
            coefs[i] = (coefs[i] - coefs[i - 1]) / (x[i] - x[i - j])
    print("Разделенная разность", coefs[-1])
    return coefs


#Норм
def newtone_infinite_differences(x, xs, ys, n):
    coefs = calculate_divided_differences(xs, ys)

    s = ys[0]

    for i in range(1, n):
        prod = 1
        for j in range(i):
            prod *= (x - xs[j])
        prod *= coefs[i]
        s += prod

    return s


def calculate_finite_differences(y):
    n = len(y)

    delta_y = [[0.0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        delta_y[i][0] = y[i]

    for j in range(1, n):
        for i in range(n - j):
            delta_y[i][j] = delta_y[i + 1][j - 1] - delta_y[i][j - 1]

    return delta_y


def print_finite_differences_table(delta_y):
    n = len(delta_y)
    print("Таблица конечных разностей:")
    for i in range(n):
        row = []
        for j in range(n-i):
            element = ""
            if delta_y[i][j] > 0:
                element += " "
            element += f"{delta_y[i][j]:.4f}"

            row.append(element)
        print("\t".join(row))


def newtone_finite_differences_1(x, xs, ys, n):
    h = xs[1] - xs[0]
    t = (x - xs[0]) / h
    coefs = calculate_finite_differences(ys)

    s = ys[0]

    for i in range(1, n):
        prod = 1.0
        for j in range(i):
            prod *= (t - j)
        prod *= (coefs[0][i] / factorial(i))
        s += prod

    return s

def newtone_finite_differences_2(x, xs, ys, n):

    h = xs[1] - xs[0]
    t = (x - xs[-1]) / h

    delta_y = calculate_finite_differences(ys)
    result = delta_y[-1][0]
    product = 1.0

    for i in range(1, n):
        product *= (t + i - 1) / i
        result += product * delta_y[-i - 1][i]

    return result


functions = {
    "Многочлен Лагранжа": lagrange,
    "Многочлен Ньютона с разделенными разностями": newtone_infinite_differences,
    "Многочлен Ньютона с конечными разностями(Формула 1)": newtone_finite_differences_1,
    "Многочлен Ньютона с конечными разностями(Формула 2)": newtone_finite_differences_2
}
