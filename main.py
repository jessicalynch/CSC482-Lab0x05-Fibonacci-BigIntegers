#!/usr/bash/bin python3

from bigintegers import BigIntegerString, BigIntegerArray
import fibbig
from time import perf_counter_ns, time_ns
from os.path import dirname, join
from math import log
import sys

# Route print statements to file
current_dir = dirname(__file__)
file_name = "output_" + str(time_ns()) + ".txt"
file_path = join(current_dir, file_name)
sys.stdout = open(file_path, "w")


def main():
    # Assign timer function to variable
    clock = perf_counter_ns

    # Determine max run time for each algorithm
    one_second = 1000000000  # 1 second in nanoseconds
    MAX_RUN_TIME = one_second * 60 * 10
    # MAX_RUN_TIME = one_second  # small value for testing
    MAX_NUMBER = 2**32 - 1

    # Build list with functions to test
    fib_funcs = [fibbig.fib_loop, fibbig.fib_matrix]
    num_funcs = len(fib_funcs)
    timed_out_funcs = [False] * num_funcs

    # Verify functions are accurate
    verify = verification_tests(fib_funcs)
    if verify:
        print("<Functions verified>\n")
    else:
        print("<Inconsistent function results>")
        exit()

    # Init table variables
    time_str = "Time"
    dr_str = "2x Ratio"
    expected_str = "Expected"
    na_str = "--"
    cols_per_func = 3  # Update if additional data columns are added
    col_width_full = 39
    col_width_med = col_width_full // cols_per_func
    col_width_small = 10

    # Print function names (header top row)
    print(f"{'':>{col_width_small * 2}}", end="")
    for i in range(num_funcs):
        print(f"{fib_funcs[i].__name__:>{col_width_full}}", end="")
    print()

    # Print data columns (header second row)
    print(f"{'x':>{col_width_small}}", end="")
    print(f"{'size':>{col_width_small}}", end="")
    for i in range(num_funcs):
        print(f"{time_str:>{col_width_med}}", end="")
        print(f"{dr_str:>{col_width_med}}", end="")
        print(f"{expected_str:>{col_width_med}}", end="")
    print("\n")

    # Init flag to track when all functions are complete
    timed_out = False

    # Init list of dictionaries to store timing results
    results = []
    for _ in range(num_funcs):
        results.append({})

    # Init list to store doubling ratios
    doubling_ratio = [-1] * num_funcs

    # Start testing algorithms with increasing x values

    for x in range(1, MAX_NUMBER):

        # Exit if all functions are complete
        if timed_out:
            print("All functions timed out")
            break

        # Otherwise assume complete and keep testing
        timed_out = True

        # Convert x to a BigIntegerArray
        big_x_to_find = BigIntegerArray(hex(x)[2:])

        # Print current x value and number of binary digits in x
        x_size = len(big_x_to_find.to_binary_list())
        print(f"{x:>{col_width_small}}", end="")
        print(f"{x_size:>{col_width_small}}", end="")

        # Loop through each function and test with current x value
        for i in range(num_funcs):

            # Skip to next function if current is timed out
            if timed_out_funcs[i]:
                # Print filler values to maintain table structure
                for _ in range(cols_per_func):
                    print(f"{na_str:>{col_width_med}}", end="")
                if i == (num_funcs - 1):
                    print()
                continue

            try:

                # Start clock
                t0 = clock()

                # Run algorithm
                fib_num = fib_funcs[i](big_x_to_find)

                # Stop clock and calculate time
                t1 = clock() - t0

                # Convert nanoseconds to milliseconds or seconds if possible
                # and print time taken for current function
                if t1 > 1000000000:
                    s = t1 // 1000000000
                    print(f"{str(s) + 's':>{col_width_med}}", end="")
                elif t1 > 1000000:
                    ms = t1 // 1000000
                    print(f"{str(ms) + 'ms':>{col_width_med}}", end="")
                else:
                    print(f"{str(t1) + 'ns':>{col_width_med}}", end="")

                # Calculate doubling ratio
                if x % 2 == 0 and x >= 4:
                    expected_dr = get_expected_dr(fib_funcs[i].__name__, x)
                    doubling_ratio[i] = t1 / results[i].pop(x // 2)
                    print(f"{doubling_ratio[i]:>{col_width_med}.2f}", end="")
                    print(f"{expected_dr:>{col_width_med}.2f}", end="")
                else:
                    print(f"{'':>{col_width_med * 2}}", end="")

                # Store time result from current run
                results[i][x] = t1

                # Update flags
                if t1 < MAX_RUN_TIME:
                    # At least one function is still going
                    timed_out = False
                else:
                    # Current function is timed out
                    timed_out_funcs[i] = True
                    results[i].clear()

            except ValueError as e:
                # Something went wrong
                print(e)
                exit()

        print()


def get_expected_dr(func_name, x):
    """Returns the expected doubling ratio for each fibonacci function"""
    if func_name == "fib_loop":  # Linear time
        # return x / (x // 2)  # or 2
        return int(2)
    elif func_name == "fib_matrix":  # Logarithmic time
        if log(x // 2, 2) > 0:
            return (log(x, 2)) / (log(x // 2, 2))
        else:
            return False


def verification_tests(funcs):
    """Verify consistent results from each function"""
    fib_results = [0] * len(funcs)

    # Find some Fibonacci numbers
    # with each function
    for x in range(1, 101):
        big_x_to_find = BigIntegerArray(hex(x)[2:])
        for i in range(len(funcs)):
            fib_results[i] = funcs[i](big_x_to_find)

        # Compare results
        for i in range(len(funcs) - 1):
            if fib_results[i].value != fib_results[i+1].value:
                return False
    return True


if __name__ == "__main__":
    main()
