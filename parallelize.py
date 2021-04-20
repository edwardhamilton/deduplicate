import multiprocessing
import os
import logging
class parallelize:
    def __init__(self, context, map, reduce, job):  # map and reduce classes must have a accept a job
        num_processes = min(context.config.num_processes, os.cpu_count() - 1)
        context.map = map
        context.reduce = reduce
        context.jobs = multiprocessing.JoinableQueue()
        context.results = multiprocessing.Queue()
        context.jobs.put(job)
        processes = []
        if (num_processes > 1):
            for i in range(num_processes):
                p = multiprocessing.Process(target=parallelize.run, args=(i, context))
                p.start()
                processes.append(p)
            context.jobs.join()  # wait until done
        else:
            parallelize.run(None, context)
        self.result = []
        while context.results.qsize():
            self.result.append(context.results.get())
        for p in processes: # must come after results queue is emptied otherwise result queue won't iterate correctly
            p.terminate()

    def run(wid, context):
        try:
            while context.jobs.qsize() > 0:
                job = context.jobs.get()
                if (context.map.done(context, job)):
                    context.results.put(context.reduce(context, job).result)
                else:
                    t = context.map(context, job)
                    for i in context.map(context, job).result:
                        context.jobs.put(i)
                context.jobs.task_done()
        except multiprocessing.TimeoutError:
            logging.info('process ' + str(_wid) + ' timedout')
        finally:
            logging.info('finally')
