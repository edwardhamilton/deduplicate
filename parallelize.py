import multiprocessing
import os
import logging

class null_reduce:
    def __init__(self):
        pass
    def run(self, job):
        return job

class parallelize:
    class _context:
        def __init__(self, map, reduce, jobs, results):
            self.map = map
            self.reduce = reduce
            self.jobs = jobs
            self.results = results
    def __init__(self, num_processes, map, reduce):  # map and reduce classes must have a run method which takes a context and job
        self.num_processes, self.map, self.reduce = num_processes, map, reduce
    def run(self, job):
        num_processes = min(self.num_processes, os.cpu_count() - 1)
        context = parallelize._context(self.map, self.reduce, jobs = multiprocessing.JoinableQueue(), results = multiprocessing.Queue())
        context.jobs.put(job)
        processes = []
        if (num_processes > 1):
            for i in range(num_processes):
                p = multiprocessing.Process(target=parallelize.worker, args=(i, context))
                p.start()
                processes.append(p)
            context.jobs.join()  # wait until done
        else:
            parallelize.worker(None, context)
        result = []
        while context.results.qsize():
            result.append(context.results.get())
        for p in processes: # must come after results queue is emptied otherwise result queue won't iterate correctly
            p.terminate()
        return result

    def worker(id, context):
        try:
            logging.debug('id = ' + str(id))
            while context.jobs.qsize() > 0:
                job = context.jobs.get()
                if (context.map.done(job)):
                    context.results.put(context.reduce.run(job))
                else:
                    for i in context.map.run(job):
                        context.jobs.put(i)
                context.jobs.task_done()
        except multiprocessing.TimeoutError:
            logging.info('process timed out')
        finally:
            logging.info('finally')
