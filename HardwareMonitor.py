import sched

__author__ = 'Dan'

import psutil
import threading
import time


class HardwareMonitor(object):
    """ Monitors the system performance of the node, used for the transfer policy. """
    SAMPLES_PER_SEC = 2
    NUM_SAMPLES = 10

    def __init__(self):
        """ Initializes the sample collections and threads necessary for scheduling. """
        super(HardwareMonitor, self).__init__()
        self.cpu_samples = [0.0] * HardwareMonitor.NUM_SAMPLES
        self.current_sample = 0
        self.monitor_thread = None
        self.monitoring = False

    def start(self):
        """ Starts the monitor thread and prevents it from ending without manually calling stop. """
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self.record_cpu)
        self.monitor_thread.start()

    def stop(self):
        """ Causes the monitor thread to finish on next execution.  Safer than killing the thread outright. """
        self.monitoring = False

    def record_cpu(self, scheduler=None):
        """ Performs a system call to record another sample of cpu utilization. """
        if scheduler is None:
            scheduler = sched.scheduler(time.time, time.sleep)
            scheduler.enter(0, 1, self.record_cpu, [scheduler])
            scheduler.run()
        else:
            self.cpu_samples[self.current_sample] = psutil.cpu_percent(0.1)
            self.current_sample = (self.current_sample + 1) % HardwareMonitor.NUM_SAMPLES

            if self.monitoring:
                scheduler.enter(1.0 / HardwareMonitor.SAMPLES_PER_SEC / 1000, 1, self.record_cpu, [scheduler])

    def get_cpu_usage(self):
        """ Calculates and returns the average CPU usage over a specific period. """
        total = 0

        for sample in self.cpu_samples:
            total += sample

        return total / HardwareMonitor.NUM_SAMPLES
