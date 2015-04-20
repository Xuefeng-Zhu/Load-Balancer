__author__ = 'Xuefeng Zhu'


class State:
    """
    Store the node state information
    """
    def __init__(self):
        self.num_jobs = 0
        self.throttling = 0
        self.cpu_usage = 0
