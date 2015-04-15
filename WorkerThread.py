__author__ = 'Dan'

import threading
import time


class WorkerThread(threading.Thread):
    """ The worker thread that executes a job on a separate thread. Could easily extend to a multi-thread. """

    def __init__(self):
        """ Initializes the worker thread with 100 throttling value and an empty current job. """
        super(WorkerThread, self).__init__()
        self.throttling = 100
        self.current_job = None
        self.timer = threading.Timer(100 * 1000, self.timer_callback)

    def run(self):
        """ This is the actual workhorse of the thread.  Executes the job if there is a current unfinished job. """
        while not self.current_job.is_finished():
            self.current_job.execute_next()

    def timer_callback(self):
        """ We will check the throttling value every second.  If we are throttled then we will sleep the thread. """
        threading.Timer(100 * 1000, self.timer_callback())
        if self.throttling < 100:
            time.sleep((100 - self.throttling) / 1000.0)







