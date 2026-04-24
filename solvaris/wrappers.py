from . import solvaris


def quadratic(a, b, c):
    x1, x2, status = solvaris.quadratic(a, b, c)
    return x1, x2


def add(a, b):
    return solvaris.add(a, b)


def sub(a, b):
    return solvaris.sub(a, b)
