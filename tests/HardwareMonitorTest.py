__author__ = 'Dan'

import unittest
import time

from Job import Job
from WorkerThread import WorkerThread
from HardwareMonitor import HardwareMonitor


class HardwareMonitorUsageTest(unittest.TestCase):
    def testHardwareMonitorTracksReasonableCpuUsage(self):
        worker_thread = WorkerThread()
        monitor = HardwareMonitor(worker_thread)

        monitor.start()
        time.sleep(2)
        monitor.stop()

        cpu_usage = monitor.get_cpu_usage()

        assert cpu_usage >= 0
        assert cpu_usage <= 100.0

    def testHardwareMonitorCpuUsageIncreasesWithWorkload(self):
        work_data = [1.111111] * 1000
        test_job = Job(work_data)
        worker_thread = WorkerThread()
        monitor = HardwareMonitor(worker_thread)

        monitor.start()
        time.sleep(2)
        clean_cpu_usage = monitor.get_cpu_usage()

        worker_thread.current_job = test_job
        worker_thread.run()

        time.sleep(2)
        dirty_cpu_usage = monitor.get_cpu_usage()

        monitor.stop()
        while worker_thread.is_alive():
            pass

        assert dirty_cpu_usage > clean_cpu_usage

    def testHardwareMonitorCpuUsageDecreasesWithThrottling(self):
        work_data = [1.111111] * 1000
        test_job_1 = Job(work_data.copy())
        test_job_2 = Job(work_data.copy())
        worker_thread = WorkerThread()
        monitor = HardwareMonitor(worker_thread)

        monitor.start()
        time.sleep(2)
        worker_thread.current_job = test_job_1
        worker_thread.run()
        full_cpu_usage = monitor.get_cpu_usage()
        monitor.stop()

        while worker_thread.is_alive():
            pass

        worker_thread.current_job = test_job_2
        worker_thread.throttling = 20
        worker_thread.run()
        time.sleep(2)
        throttled_cpu_usage = monitor.get_cpu_usage()
        monitor.stop()

        while worker_thread.is_alive():
            pass

        assert throttled_cpu_usage < full_cpu_usage


if __name__ == '__main__':
    unittest.main()
