__author__ = 'Xuefeng Zhu'


class State:

    def __init__(self):
        self.num_jobs = 0
        self.throttling = 0
        self.cpu_usage = 0

    def update_state(self, num_jobs, throttling, cpu_usage):
        self.num_jobs = num_jobs
        self.throttling = throttling
        self.cpu_usage = cpu_usage
