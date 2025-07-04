from typing import Callable, List


def improved_euler_method(f: Callable, xs: List[float], y0: float) -> List[float]:
    ys = [y0]
    h = xs[1] - xs[0]
    for i in range(len(xs) - 1):
        y_pred = ys[i] + h * f(xs[i], ys[i])
        ys.append(ys[i] + 0.5 * h * (f(xs[i], ys[i]) + f(xs[i + 1], y_pred)))
    return ys


def fourth_order_runge_kutta_method(f: Callable, xs: List[float], y0: float) -> List[float]:
    ys = [y0]
    h = xs[1] - xs[0]
    for i in range(len(xs) - 1):
        k1 = h * f(xs[i], ys[i])
        k2 = h * f(xs[i] + h / 2, ys[i] + k1 / 2)
        k3 = h * f(xs[i] + h / 2, ys[i] + k2 / 2)
        k4 = h * f(xs[i] + h, ys[i] + k3)
        ys.append(ys[i] + (k1 + 2 * k2 + 2 * k3 + k4) / 6)
    return ys


def adams(f: Callable, xs: List[float], y0: float, eps: float) -> List[float]:
    if len(xs) < 4:
        raise ValueError("Для метода Адамса требуется минимум 4 точки")

    ys = fourth_order_runge_kutta_method(f, xs[:4], y0)[:4]
    h = xs[1] - xs[0]

    for i in range(3, len(xs) - 1):
        f_prev = [f(xs[j], ys[j]) for j in range(i - 3, i + 1)]
        # Предиктор
        y_pred = ys[i] + h * (55 * f_prev[3] - 59 * f_prev[2] + 37 * f_prev[1] - 9 * f_prev[0]) / 24

        while True:
            # Корректор
            f_corr = f(xs[i + 1], y_pred)
            y_corr = ys[i] + h * (9 * f_corr + 19 * f_prev[3] - 5 * f_prev[2] + f_prev[1]) / 24
            if abs(y_corr - y_pred) < eps:
                break
            y_pred = y_corr
        ys.append(y_pred)

    return ys