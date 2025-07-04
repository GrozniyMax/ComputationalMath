from math import sqrt


def mean(values) -> float:
    return sum(values) / len(values)


def correlation(X, Y):
    x_mean = mean(X)
    y_mean = mean(Y)

    y_sums = [(y - y_mean) for y in Y]
    x_sums = [(x - x_mean) for x in X]

    numerator = sum([(x_i * y_i) for x_i, y_i in zip(x_sums, y_sums)])
    denominator = sum([x_i**2 for x_i in X])
    denominator *= sum([y_i**2 for y_i in Y])
    denominator = sqrt(denominator)

    return numerator / denominator

def mnk(f, x, X, Y) -> float:
    return sum([(f.subs(x, x_i) - y_i).evalf() ** 2 for x_i, y_i in zip(X, Y)])

def mean_square_deviation(f, x, X, Y):
    numerator = mnk(f, x, X, Y)
    denominator = len(X)
    return sqrt(numerator / denominator)


def determination_coef(f, x, X, Y):
    numerator = mnk(f, x, X, Y)
    phi_mean = mean([f.subs(x, x_i).evalf() for x_i in X])
    denominator = sum([(y - phi_mean)**2 for  y in Y])

    result = 1 - (numerator/denominator)
    if result < 0:
        result = 0
    return result

