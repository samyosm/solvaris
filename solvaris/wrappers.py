from . import solvaris


def quadratic(a, b, c):
    x1, x2, status = solvaris.quadratic(a, b, c)
    if status == 0 or status == -2:
        raise "Error"
    elif status == 1:
        return x1
    elif status == 2:
        return x1, x2
    raise "Unkown status"


def add(a, b):
    return solvaris.add(a, b)


def sub(a, b):
    return solvaris.sub(a, b)
