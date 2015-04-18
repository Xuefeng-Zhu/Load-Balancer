import sched
import subprocess
import psutil
import threading
import time

__author__ = 'Dan'


class HardwareMonitor(object):
    """ Monitors the system performance of the node,
     used for the transfer policy.
    """
    SAMPLES_PER_SEC = 5
    NUM_SAMPLES = 10
    NETWORK_DELAY = 0

    def __init__(self, worker_thread):
        """ Initializes the sample collections and threads
        necessary for scheduling.
        """
        super(HardwareMonitor, self).__init__()
        self.monitoring = False
        self.cpu_samples = [0.0] * HardwareMonitor.NUM_SAMPLES
        self.current_sample = 0
        self.monitor_thread = None

        self.worker_thread = worker_thread

    def start(self):
        """ Starts the monitor thread and prevents it from ending
        without manually calling stop.
        """
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self.record_cpu)
        self.monitor_thread.start()

    def stop(self):
        """ Causes the monitor thread to finish on next execution.
        Safer than killing the thread outright.
        """
        self.monitoring = False
        self.cpu_samples = [0.0] * HardwareMonitor.NUM_SAMPLES

    def throttle(self, value):
        """ Interface for throttling the worker thread through 
        the hardware monitor. 
        """
        self.worker_thread.throttling = value

    def record_cpu(self, scheduler=None):
        """ Performs a system call to record another sample of cpu utilization. """
        if scheduler is None:
            scheduler = sched.scheduler(time.time, time.sleep)
            scheduler.enter(0, 1, self.record_cpu, [scheduler])
            scheduler.run()
        else:
            self.cpu_samples[self.current_sample] = psutil.cpu_percent()
            self.current_sample = (
                self.current_sample + 1) % HardwareMonitor.NUM_SAMPLES

            if self.monitoring:
                scheduler.enter(
                    1.0 / HardwareMonitor.SAMPLES_PER_SEC / 1000, 1, self.record_cpu, [scheduler])

    def get_cpu_usage(self):
        """ Calculates and returns the average CPU usage over a specific period. """
        total = 0

        for sample in self.cpu_samples:
            total += sample

        return total / HardwareMonitor.NUM_SAMPLES

    def calculate_network_delay(self, ip):
        """ Returns the average ping between the nodes. """
        p = subprocess.Popen(["ping.exe", ip], stdout=subprocess.PIPE)
        out_text = p.communicate()[0]

        l_search_string = "Average = "
        r_search_string = "ms"
        l_index = out_text.rfind(l_search_string.encode())
        r_index = out_text.rfind(r_search_string.encode())
        delay_text = out_text[l_index + len(l_search_string):r_index]

        HardwareMonitor.NETWORK_DELAY = int(delay_text)
