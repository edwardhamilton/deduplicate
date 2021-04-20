import statistics
import parallelize
class map:
    def __init__(self, context, job):
        self.context = context
        self.result = []
        median = statistics.median(job)
        self.result.append(list(filter(lambda x: x <= median, job)))
        self.result.append(list(filter(lambda x: x > median, job)))
    def done(context, job):
        return len(job) <= context.partition_size
class reduce:
    def __init__(self, context, job):
        self.result = [i * context.multiply_by for i in job]


class context:
    class config:
        def __init__(self):
            self.num_processes = 2
    def __init__(self):
        self.partition_size = 2
        self.multiply_by = 10
        self.config = self.config()
if __name__ == '__main__':
    print(parallelize.parallelize(context(), map, reduce, list(range(0, 100000))).result)
