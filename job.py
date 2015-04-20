__author__ = 'Dan'


class Job(object):
    """ A simple data structure which contains the data
    and handles the workload for MP4.
    """
    ITER_COUNT = 1000

    def __init__(self, id=0, pos=0, work_data=[]):
        """ Initializes private variables and work data. """
        self.id = id
        self.pos = pos
        self.work_data = work_data
        self.current_element = 0
        self.current_iteration = 0

    def execute_next(self):
        """ Does the MP4 computation. Do not optimize. """
        for _ in range(Job.ITER_COUNT):
            self.work_data[self.current_element] += 1.111111

        if self.current_element < len(self.work_data):
            self.current_element += 1

    def is_finished(self):
        """ Returns true if every element in the work_data has been
        processed.
        """
        return self.current_element == len(self.work_data)
