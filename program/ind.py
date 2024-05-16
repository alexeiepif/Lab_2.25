#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Задание 2.23
# С использованием многопоточности для
# заданного значения x найти сумму ряда S с
# точностью члена ряда по абсолютному
# значению e=10^-7 и произвести сравнение полученной суммы
# с контрольным значением функции y
# для двух бесконечных рядов.
# Варианты 9 и 10

# Задание 2.25
# Для своего индивидуального задания лабораторной работы 2.23
# необходимо реализовать вычисление значений
# в двух функций в отдельных процессах.

import math
from multiprocessing import Barrier, Manager, Process


# 10 V
def sum1(x, eps, s_dict, br, lock):
    s = 0
    n = 0
    while True:
        k = 2 * n
        term = x**k / math.factorial(k)
        if abs(term) < eps:
            break
        else:
            s += term
            n += 1
    with lock:
        s_dict["s1"] = s
    br.wait()


# 9 V
def sum2(x, eps, s_dict, br, lock):
    s = 0
    n = 0
    while True:
        k = 2 * n + 1
        term = (-1) ** n * x**k / math.factorial(k)
        if abs(term) < eps:
            break
        else:
            s += term
            n += 1
    with lock:
        s_dict["s2"] = s
    br.wait()


def compair(s, y1, y2, br):
    br.wait()
    s1 = s["s1"]
    s2 = s["s2"]

    print(
        f"Сумма 10 Варианта: {s1},"
        f" Ожидаемое значение y1: {y1}, Разница: {abs(s1 - y1)}"
    )
    print(
        f"Сумма 9 Варианта: {s2},"
        f" Ожидаемое значение y2: {y2}, Разница: {abs(s2 - y2)}"
    )


def main(m):
    s = m.dict()

    br = Barrier(3)
    lock = m.Lock()

    eps = 10**-7
    # 10 V
    x1 = 1 / 2
    y1 = (math.e**x1 + math.e**-x1) / 2
    # 9 V
    x2 = 1.4
    y2 = math.sin(x2)

    process1 = Process(target=sum1, args=(x1, eps, s, br, lock))
    process2 = Process(target=sum2, args=(x2, eps, s, br, lock))
    process3 = Process(target=compair, args=(s, y1, y2, br))

    # Запуск потоков
    process1.start()
    process2.start()
    process3.start()

    process1.join()
    process2.join()
    process3.join()


if __name__ == "__main__":
    with Manager() as manager:
        main(manager)
