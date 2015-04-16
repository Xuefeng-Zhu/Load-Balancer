import math
from JobQueue import JobQueue

__author__ = 'Dan'

import unittest
import time

from Job import Job
from WorkerThread import WorkerThread


class WorkerThreadExecutionTest(unittest.TestCase):
    def testWorkerThreadExecutesJob(self):
        work_data = [1.111111] * 5
        test_job = [Job(work_data)]
        job_queue = JobQueue()
        job_queue.add_jobs(test_job)
        worker_thread = WorkerThread(job_queue)

        worker_thread.run()

        while worker_thread.is_alive():
            pass

        assert math.fabs(test_job[0].work_data[0] - 1.111111 * 1001) < 1
        assert math.fabs(test_job[0].work_data[-1] - 1.111111 * 1001) < 1

    def testWorkerThreadExecutesSequentialJobs(self):
        work_data_1 = [1.111111] * 5
        work_data_2 = [0] * 5
        test_jobs = [Job(work_data_1), Job(work_data_2)]
        job_queue = JobQueue()
        job_queue.add_jobs(test_jobs)
        worker_thread = WorkerThread(job_queue)

        worker_thread.run()

        while worker_thread.is_alive():
            pass

        assert math.fabs(test_jobs[0].work_data[0] - 1.111111 * 1001) < 1
        assert math.fabs(test_jobs[1].work_data[-1] - 1.111111 * 1000) < 1

    def testWorkerThreadThrottleIncreasesExecutionTime(self):
        work_data_1 = [1.111111] * 100
        work_data_2 = [1.111111] * 100
        test_jobs = [Job(work_data_1), Job(work_data_2)]
        job_queue = JobQueue()
        job_queue.add_jobs(test_jobs)
        worker_thread = WorkerThread(job_queue)

        start_time = time.time()
        worker_thread.run()

        while worker_thread.is_alive():
            pass

        unthrottled_execution_time = time.time() - start_time

        work_data_1 = [1.111111] * 100
        work_data_2 = [1.111111] * 100
        test_jobs = [Job(work_data_1), Job(work_data_2)]
        job_queue = JobQueue()
        job_queue.add_jobs(test_jobs)
        worker_thread = WorkerThread(job_queue)
        worker_thread.throttling = 50

        start_time = time.time()
        worker_thread.run()

        while worker_thread.is_alive():
            pass

        throttled_execution_time = time.time() - start_time

        assert unthrottled_execution_time < throttled_execution_time


if __name__ == '__main__':
    unittest.main()
