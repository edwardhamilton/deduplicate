import statistics
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
        return [i * self.multiply_by for i in job]


if __name__ == '__main__':
    print(parallelize.parallelize(num_processes=12, map = map(4), reduce = reduce(10), job=list(range(0, 100000))).result)
