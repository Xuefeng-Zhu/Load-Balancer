__author__ = 'Dan'

import psutil
import threading


class HardwareMonitor(object):
    """ Monitors the system performance of the node, used for the transfer policy. """
    SAMPLES_PER_100 = 5
    NUM_SAMPLES = 10

    def __init__(self):
        """ Initializes the sample collections. """
        self.cpu_samples = [None] * HardwareMonitor.NUM_SAMPLES
        self.current_sample = 0

        self.timer = threading.Timer(100.0 * 1000, self.cpu_record())

    def cpu_record(self):
        """ Performs a system call to record another sample of cpu utilization. """
        self.cpu_samples[self.current_sample] = psutil.cpu_percent()
        self.current_sample = (self.current_sample + 1) % HardwareMonitor.NUM_SAMPLES

        self.timer = threading.Timer(100.0 * 1000, self.cpu_record())

    def get_cpu_usage(self):
        """ Calculates and returns the average CPU usage over a specific period. """
        total = 0
        for sample in self.cpu_samples:
            total += sample

        return total / HardwareMonitor.NUM_SAMPLES


