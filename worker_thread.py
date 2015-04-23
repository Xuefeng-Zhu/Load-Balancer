__author__ = 'Dan'

import threading
import time


class WorkerThread(threading.Thread):
    """ The worker thread that executes a job on a separate thread. Could easily extend to a multi-thread. """

    def __init__(self, job_queue, launcher):
        """ Initializes the worker thread with 100 throttling value and an empty current job. """
        super(WorkerThread, self).__init__()
        self.job_queue = job_queue
        self.launcher = launcher
        self.throttling = 100
        self.current_job = None

    def run(self):
        """ This is the actual workhorse of the thread.  Executes the job if there is a current unfinished job. """
        start_time = time.time()
        while self.job_queue.qsize() > 0:
            self.current_job = self.job_queue.get()
            while not self.current_job.is_finished():
                if time.time() - start_time < self.throttling / 1000.0:
                    self.current_job.execute_next()
                else:
                    time.sleep((100 - self.throttling) / 1000.0)
                    start_time = time.time()
			
			print "Job %d finished" % (self.current_job.id)
            self.launcher.on_job_finish(self.current_job)
