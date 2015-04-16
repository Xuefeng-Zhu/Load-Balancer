__author__ = 'Dan'

import unittest
import time

from Job import Job
from WorkerThread import WorkerThread
from HardwareMonitor import HardwareMonitor


class HardwareMonitorUsageTest(unittest.TestCase):
    def testHardwareMonitorTracksReasonableCpuUsage(self):
        monitor = HardwareMonitor()

        monitor.start()
        time.sleep(1)
        monitor.stop()

        cpu_usage = monitor.get_cpu_usage()

        assert cpu_usage > 0
        assert cpu_usage < 100.0

    def testHardwareMonitorCpuUsageIncreasesWithWorkload(self):
        work_data = [1.111111] * 1000
        test_job = Job(work_data)
        worker_thread = WorkerThread()
        monitor = HardwareMonitor()

        monitor.start()
        time.sleep(1)
        clean_cpu_usage = monitor.get_cpu_usage()

        worker_thread.current_job = test_job
        worker_thread.run()

        time.sleep(1)
        dirty_cpu_usage = monitor.get_cpu_usage()

        monitor.stop()
        while worker_thread.is_alive():
            pass

        assert dirty_cpu_usage > clean_cpu_usage


if __name__ == '__main__':
    unittest.main()
