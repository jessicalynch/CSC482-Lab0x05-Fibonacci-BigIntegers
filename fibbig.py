#!/usr/bin/env python3

"""fibbig.py: fibonacci sequence functions with BigIntegerArray class"""
__author__ = "Jessica Lynch"

from bigintegers import BigIntegerArray


def fib_loop(x):
    """Returns xth value in fibonacci sequence via iteration"""
    if x.value == [1]:
        return BigIntegerArray("0")
    else:
        a = BigIntegerArray("0")
        b = BigIntegerArray("1")

        # TODO: remove dependency on to_int()
        for i in range(2, x.to_int()):
            next_int = a + b
            a = b
            b = next_int
        return b


def fib_matrix(x):
    """Returns xth value in fibonacci sequence via matrix multiplication"""
    if x.value == [1]:
        return BigIntegerArray("0")
    else:
        one = BigIntegerArray("1")
        zero = BigIntegerArray("0")
        m = [[one, one],
             [one, zero]]  # magic matrix
        result = matrix_power(m, x)
        return result[1][1]


def matrix_multiply(m1, m2):
    """Multiplies two matrices together"""
    if len(m1[0]) != len(m2):
        return False
    # List comprehension method
    # made possible by __radd__ being overloaded
    # in BigIntegerArray class ("reverse add" used by sum())
    return [[sum(a * b for a, b in zip(m1_row, m2_col)) for m2_col in zip(*m2)] for m1_row in m1]

    # Nested loop method
    # m3 = []  # Return matrix
    # for _ in range(len(m1)):
    #     m3.append([BigIntegerArray("0")] * len(m2[0]))
    #
    # for i in range(len(m1)):
    #     for j in range(len(m2[0])):
    #         result = BigIntegerArray("0")
    #         for k in range(len(m2)):
    #             result += m1[i][k] * m2[k][j]
    #         m3[i][j] = result
    # return m3


def matrix_power(m, y):
    """Returns matrix raised to a power"""
    binary_digits = y.to_binary_list()
    binary_digits.reverse()

    # Create the matrix equivalent to BigIntegerArray("1")
    n = len(m)
    identity_matrix = [[BigIntegerArray(hex(int(i == j))[2:])
                        for i in range(n)] for j in range(n)]
    # Init return matrix with identity matrix
    product = identity_matrix

    # Loop through the binary digits
    for digit in binary_digits:
        # If the digit is a 1, multiply by the current matrix power
        if digit:
            product = matrix_multiply(product, m)

        # Square the matrix every time to increase the power
        m = matrix_multiply(m, m)
    return product


def matrix_print(m):
    """Prints a matrix"""
    for i in range(len(m)):
        for j in range(len(m[i])):
            print(f"{m[i][j].value} ", end="")
        print()
