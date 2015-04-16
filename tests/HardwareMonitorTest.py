from JobQueue import JobQueue

__author__ = 'Dan'

import unittest
import time

from Job import Job
from WorkerThread import WorkerThread
from HardwareMonitor import HardwareMonitor


class HardwareMonitorUsageTest(unittest.TestCase):
    def testHardwareMonitorTracksReasonableCpuUsage(self):
        monitor = HardwareMonitor(None)

        monitor.start()
        time.sleep(2)
        monitor.stop()

        cpu_usage = monitor.get_cpu_usage()

        assert cpu_usage >= 0
        assert cpu_usage <= 100.0

    def testHardwareMonitorCpuUsageIncreasesWithWorkload(self):
        work_data = [1.111111] * 1000
        test_job = [Job(work_data)]
        job_queue = JobQueue()
        job_queue.add_jobs(test_job)
        worker_thread = WorkerThread(job_queue)
        monitor = HardwareMonitor(worker_thread)

        monitor.start()
        time.sleep(0.5)
        clean_cpu_usage = monitor.get_cpu_usage()

        worker_thread.run()
        while worker_thread.is_alive():
            pass
        dirty_cpu_usage = monitor.get_cpu_usage()
        monitor.stop()

        assert dirty_cpu_usage > clean_cpu_usage

    def testHardwareMonitorCpuUsageDecreasesWithThrottling(self):
        work_data_1 = [1.111111] * 1000
        work_data_2 = [1.111111] * 1000
        test_jobs = [Job(work_data_1), Job(work_data_2)]
        job_queue = JobQueue()
        job_queue.add_jobs(test_jobs)
        worker_thread = WorkerThread(job_queue)
        monitor = HardwareMonitor(worker_thread)

        monitor.start()
        worker_thread.run()
        while worker_thread.is_alive():
            pass
        full_cpu_usage = monitor.get_cpu_usage()
        monitor.stop()

        work_data_1 = [1.111111] * 1000
        work_data_2 = [1.111111] * 1000
        test_jobs = [Job(work_data_1), Job(work_data_2)]
        job_queue = JobQueue()
        job_queue.add_jobs(test_jobs)
        worker_thread = WorkerThread(job_queue)
        worker_thread.throttling = 20

        monitor.start()
        worker_thread.run()
        while worker_thread.is_alive():
            pass

        throttled_cpu_usage = monitor.get_cpu_usage()
        monitor.stop()

        assert throttled_cpu_usage < full_cpu_usage

    def testNetworkDelay(self):
        monitor = HardwareMonitor(None)
        monitor.calculate_network_delay("www.google.com")
        assert HardwareMonitor.NETWORK_DELAY > 0

if __name__ == '__main__':
    unittest.main()
