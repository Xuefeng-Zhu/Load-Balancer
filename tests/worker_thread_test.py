import math
import unittest
import time

from job import Job
from worker_thread import WorkerThread
from Queue import Queue
from launcher import Launcher
__author__ = 'Dan'


class WorkerThreadExecutionTest(unittest.TestCase):
    def testWorkerThreadExecutesJob(self):
        work_data = [1.111111] * 5
        test_job = Job(0, 0, work_data)
        job_queue = Queue()
        job_queue.put(test_job)
        launcher = Launcher(True, None, None)
        worker_thread = WorkerThread(job_queue, launcher)

        worker_thread.run()

        while worker_thread.is_alive():
            pass

        assert math.fabs(test_job.work_data[0] - 1.111111 * 1001) < 1
        assert math.fabs(test_job.work_data[-1] - 1.111111 * 1001) < 1

    def testWorkerThreadExecutesSequentialJobs(self):
        work_data_1 = [1.111111] * 5
        work_data_2 = [0] * 5
        test_jobs = [Job(0, 0, work_data_1), Job(0, 0, work_data_2)]
        job_queue = Queue()
        job_queue.put(test_jobs[0])
        job_queue.put(test_jobs[1])
        worker_thread = WorkerThread(job_queue, None)

        try:
            worker_thread.run()
        except:
            pass

        while worker_thread.is_alive():
            pass

        self.assertEqual(int(test_jobs[0].work_data[0]), 1112)
        self.assertEqual(int(test_jobs[1].work_data[0]), 0)

    def testWorkerThreadThrottleIncreasesExecutionTime(self):
        work_data_1 = [1.111111] * 100
        work_data_2 = [1.111111] * 100
        test_jobs = [Job(0, 0, work_data_1), Job(0, 0, work_data_2)]
        job_queue = Queue()
        job_queue.put(test_jobs[0])
        job_queue.put(test_jobs[1])
        worker_thread = WorkerThread(job_queue, None)

        start_time = time.time()
        try:
            worker_thread.run()
        except:
            pass

        while worker_thread.is_alive():
            pass

        unthrottled_execution_time = time.time() - start_time

        work_data_1 = [1.111111] * 100
        work_data_2 = [1.111111] * 100
        test_jobs = [Job(0, 0, work_data_1), Job(0, 0, work_data_2)]
        job_queue = Queue()
        job_queue.put(test_jobs[0])
        job_queue.put(test_jobs[1])
        worker_thread = WorkerThread(job_queue, None)
        worker_thread.throttling = 50

        start_time = time.time()
        try:
            worker_thread.run()
        except:
            pass

        while worker_thread.is_alive():
            pass

        throttled_execution_time = time.time() - start_time

        assert unthrottled_execution_time < throttled_execution_time


if __name__ == '__main__':
    unittest.main()
