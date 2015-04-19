"""
Just use python Queue
"""
import queue

__author__ = 'Dan'


class JobQueue(object):
    """ A queue to manage unfinished jobs for the worker thread and transfer manager. """

    def __init__(self):
        """ Initializes an empty job queue. """
        self.job_list = []
        self.event_queue = queue.Queue()

    def get_length(self):
        """ Returns the number of remaining jobs. """
        return len(self.job_list)

    def is_empty(self):
        """" Returns if the job queue has zero jobs left. """
        return len(self.job_list) == 0

    def add_jobs(self, new_jobs):
        """ Adds a list of jobs to the queue. """
        self.job_list.extend(new_jobs)

    def pop_next_job(self):
        """ Gets the next job from the queue and pops it off. """
        popped_job = self.job_list[0]
        del self.job_list[0]

        return popped_job

    def pop_jobs(self, number):
        """ Pops up to the specified number of jobs from the queue and returns them. """
        end_index = min(number, len(self.job_list))
        popped_jobs = self.job_list[0:end_index]
        del self.job_list[0:end_index]

        return popped_jobs
