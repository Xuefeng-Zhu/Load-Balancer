import math

__author__ = 'Dan'

import unittest
import time

from Job import Job
from WorkerThread import WorkerThread


class WorkerThreadExecutionTest(unittest.TestCase):
    def testWorkerThreadExecutesJob(self):
        work_data = [1.111111] * 5
        test_job = Job(work_data)
        worker_thread = WorkerThread()

        worker_thread.current_job = test_job
        worker_thread.run()

        while worker_thread.is_alive():
            pass

        assert math.fabs(test_job.work_data[0] - 1.111111 * 1001) < 1
        assert math.fabs(test_job.work_data[-1] - 1.111111 * 1001) < 1

    def testWorkerThreadExecutesSequentialJobs(self):
        work_data_1 = [1.111111] * 5
        work_data_2 = [0] * 5
        test_job_1 = Job(work_data_1)
        test_job_2 = Job(work_data_2)
        worker_thread = WorkerThread()

        worker_thread.current_job = test_job_1
        worker_thread.run()

        while worker_thread.is_alive():
            pass

        worker_thread.current_job = test_job_2
        worker_thread.run()

        while worker_thread.is_alive():
            pass

        assert math.fabs(test_job_1.work_data[0] - 1.111111 * 1001) < 1
        assert math.fabs(test_job_2.work_data[0] - 1.111111 * 1000) < 1

    def testWorkerThreadThrottleIncreasesExecutionTime(self):
        work_data = [1.111111] * 100
        test_job_1 = Job(work_data.copy())
        test_job_2 = Job(work_data.copy())
        worker_thread = WorkerThread()
        worker_thread.current_job = test_job_1

        start_time = time.time()
        worker_thread.run()

        while not test_job_1.is_finished():
            pass

        unthrottled_execution_time = time.time() - start_time

        worker_thread = WorkerThread()
        worker_thread.current_job = test_job_2
        worker_thread.throttling = 50

        start_time = time.time()
        worker_thread.run()

        while not test_job_2.is_finished():
            pass

        throttled_execution_time = time.time() - start_time

        assert unthrottled_execution_time < throttled_execution_time


if __name__ == '__main__':
    unittest.main()
