import unittest
import time

from job import Job
from worker_thread import WorkerThread
from hardware_monitor import HardwareMonitor
from Queue import Queue

__author__ = 'Dan'


class MockLauncher:
    def on_job_finish(self, job):
        pass


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
        test_job = Job(0, 0, work_data)
        job_queue = Queue()
        job_queue.put(test_job)
        launcher = MockLauncher()
        worker_thread = WorkerThread(job_queue, launcher)
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
        test_jobs = [Job(0, 0, work_data_1), Job(0, 0, work_data_2)]
        job_queue = Queue()
        job_queue.put(test_jobs[0])
        job_queue.put(test_jobs[1])
        launcher = MockLauncher()
        worker_thread = WorkerThread(job_queue, launcher)
        monitor = HardwareMonitor(worker_thread)

        monitor.start()
        try:
            worker_thread.run()
        except:
            pass
        while worker_thread.is_alive():
            pass
        full_cpu_usage = monitor.get_cpu_usage()
        monitor.stop()

        work_data_1 = [1.111111] * 1000
        work_data_2 = [1.111111] * 1000
        test_jobs = [Job(0, 0, work_data_1), Job(0, 0, work_data_2)]
        job_queue = Queue()
        job_queue.put(test_jobs[0])
        job_queue.put(test_jobs[1])
        launcher = MockLauncher()
        worker_thread = WorkerThread(job_queue, launcher)
        worker_thread.throttling = 20

        monitor.start()
        try:
            worker_thread.run()
        except:
            pass
        while worker_thread.is_alive():
            pass

        throttled_cpu_usage = monitor.get_cpu_usage()
        monitor.stop()

        assert throttled_cpu_usage < full_cpu_usage

    def testNetworkDelay(self):
        monitor = HardwareMonitor(None)
        # monitor.calculate_network_delay("www.google.com")
        # assert HardwareMonitor.NETWORK_DELAY > 0


if __name__ == '__main__':
    unittest.main()
