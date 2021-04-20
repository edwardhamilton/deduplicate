class parallelize:
    def __init__(self, context, map, reduce, job):  # map and reduce classes must have a accept a job
        self.num_processes = min(context.config.num_processes, os.cpu_count() - 1)
        self.map = map
        self.reduce = reduce
        self.context = context
        self.jobs = multiprocessing.JoinableQueue()
        self.results = multiprocessing.Queue()
        self.jobs.put(job)
        processes = []
        if (num_processes > 1):
            for i in range(num_processes):
                p = multiprocessing.Process(target=self.run, args=(i, self.parent))
                p.start()
                processes.append(p)
            self.jobs.join()  # wait until done
        else:
            self.run(None, self)
        self.result = []
        while self.results.qsize():
            self.result.append(self.results.get())
		for p in processes: # must come after results queue is emptied otherwise result queue won't iterate correctly
			p.terminate()
			
    def run(self, wid, parent):
        try:
            while parent.jobs.qsize() > 0:
                job = parent.jobs.get()
                if (map.done(job)):
                    parent.results.put(parent.reduce(context, job).result)
                else:
                    t = parent.map(parent, job)
                    for i in parent.map(context, job).result:
                        parent.jobs.put(i)
                parent.jobs.task_done()
        except multiprocessing.TimeoutError:
            print('process ' + str(_wid) + ' timedout')
        finally:
            trace('finally')
