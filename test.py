#!/usr/bin/env python3

import array
import random
import statistics
import struct
import time

import numpy as np

# Generate a list of length 400,000
LIST_TEST_SIZE = 400_000
TEST_DATA = [random.random() for _ in range(LIST_TEST_SIZE)]
NP_TEST_DATA = np.random.rand(LIST_TEST_SIZE)
ITERATIONS_LIST = [2, 10, 100, 1_000]  # , 10_000, 100_000, 1_000_000]


def timing_decorator(func):
    def wrapper(*args, **kwargs):
        run_times = []
        num_runs = None

        for num_iterations in ITERATIONS_LIST:
            num_runs = num_iterations
            start_time = time.perf_counter()

            for _ in range(num_iterations):
                func(*args, **kwargs)

                end_time = time.perf_counter()
                run_times.append(end_time - start_time)

            avg_time = sum(run_times) / len(run_times)
            std_dev = statistics.stdev(run_times)

            print(
                f"Function '{func.__name__}' (Avg. of {num_runs} runs, {num_iterations} iterations/run):"
            )
            print(f"  - Average time: {avg_time:.6f} seconds")
            print(f"  - Standard deviation: {std_dev:.6f} seconds")

        return func(*args, **kwargs)

    return wrapper


@timing_decorator
def original_pack(float_array):
    return b"".join(struct.pack("f", f) for f in float_array)


@timing_decorator
def original_unpack(value):
    if value:
        num_floats = len(value) // 4
        return struct.unpack(f"{num_floats}f", value)
    else:
        return None


@timing_decorator
def early_exit_unpack(value):
    if not value:
        return None

    num_floats = len(value) // 4
    return struct.unpack(f"{num_floats}f", value)


@timing_decorator
def no_fstring_unpack(value):
    if value:
        num_floats = len(value) // 4
        unpack_string = "f" * num_floats
        return struct.unpack(unpack_string, value)
    else:
        return None


@timing_decorator
def np_pack(float_array):
    return float_array.tobytes()


@timing_decorator
def np_unpack(value):
    if value:
        num_floats = len(value) // 4
        return np.frombuffer(value, dtype=np.float32, count=num_floats)
    else:
        return None


@timing_decorator
def array_pack(float_array):
    return array.array("f", float_array).tobytes()


@timing_decorator
def array_unpack(value):
    if value:
        return array.array("f", value)
    else:
        return None


if __name__ == "__main__":
    original_packed_data = original_pack(TEST_DATA)
    dump = original_unpack(original_packed_data)
    dump = early_exit_unpack(original_packed_data)
    dump = no_fstring_unpack(original_packed_data)
    dump = np_unpack(np_pack(NP_TEST_DATA))
    dump = array_unpack(array_pack(TEST_DATA))
