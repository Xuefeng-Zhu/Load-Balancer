__author__ = 'Dan'


class Job(object):

    """ A simple data structure which contains the data
    and handles the workload for MP4.
    """
    ITER_COUNT = 1000

    def __init__(self, pos, work_data):
        """ Initializes private variables and work data. """
        self.pos = pos
        self.work_data = work_data
        self.current_element = 0
        self.current_iteration = 0

    def execute_next(self):
        """ Does the MP4 computation. Do not optimize. """
        self.work_data[self.current_element] += 1.111111

        self.current_iteration += 1
        if self.current_iteration == Job.ITER_COUNT:
            self.current_element += 1
            self.current_iteration = 0

    def is_finished(self):
        """ Returns true if every element in the work_data has been
        processed.
        """
        return self.current_element == len(self.work_data)
