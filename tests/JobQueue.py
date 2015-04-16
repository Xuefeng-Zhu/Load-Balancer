__author__ = 'Dan'


class JobQueue(object):
    """ A queue to manage unfinished jobs for the worker thread and transfer manager. """

    def __init__(self):
        self.job_list = []

    def add_jobs(self, new_jobs):
        """ Adds a list of jobs to the queue. """
        self.job_list.extend(new_jobs)

    def pop_jobs(self, number):
        """ Pops up to the specified number of jobs from the queue and returns them. """
        end_index = min(number, len(self.job_list) - 1) - 1
        popped_jobs = self.job_list[1:end_index]
        del self.job_list[1:end_index]

        return popped_jobs
