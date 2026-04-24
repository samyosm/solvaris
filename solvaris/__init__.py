from . import _solvaris


def quadratic(a, b, c):
    x1, x2, status = _solvaris.quadratic(a, b, c)
    return x1, x2


def add(a, b):
    return _solvaris.add(a, b)


def sub(a, b):
    return _solvaris.sub(a, b)
