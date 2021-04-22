import statistics
import math
import unittest
import time
import sys
sys.path.append('../')
import parallelize


class map:
    def __init__(self, partition_size):
        self.partition_size = partition_size
    def run(self, job):
        result = []
        median = statistics.median(job)
        result.append(list(filter(lambda x: x <= median, job)))
        result.append(list(filter(lambda x: x > median, job)))
        return result
    def done(self, job):
        return len(job) <= self.partition_size
class reduce:
    def __init__(self, multiply_by):
        self.multiply_by = multiply_by
    def run(self, job):
        temp = 12343
        for i in range(0, 2000):  # consume some CPU
            temp = temp + math.sqrt(i)
        return [((i * self.multiply_by) + temp) for i in job]

def test_paralellize(num_processes):
    start = time.perf_counter()
    result = parallelize.parallelize(num_processes=num_processes, map = map(4), reduce = reduce(10), job=list(range(0, 100000)))
    runtime = time.perf_counter() - start
    return runtime, result


class Test_Parallelize(unittest.TestCase):

    def test_parallelized_fasterwithmoreprocesses(self):
        runtime_1process, result_1process = test_paralellize(1)
        runtime_6process, result_6process = test_paralellize(6)
        self.assertTrue(runtime_6process < (0.4 * runtime_1process))
        self.assertEqual(result_1process.result, result_6process.result)


if __name__ == '__main__':
    unittest.main()
