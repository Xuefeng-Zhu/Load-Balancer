from job import Job

__author__ = 'Dan'

import unittest

from job_queue import JobQueue


class JobQueueJobsTest(unittest.TestCase):
    def testJobQueueHoldsJob(self):
        queue = JobQueue()
        jobs = [Job(None)]

        queue.add_jobs(jobs)

        assert queue.pop_next_job() == jobs[0]

    def testJobQueueHoldsMultipleJobs(self):
        queue = JobQueue()
        jobs = [Job(None), Job(None)]

        queue.add_jobs(jobs)

        assert queue.pop_next_job() == jobs[0]
        assert queue.pop_next_job() == jobs[1]

    def testJobQueueEmptyAndNotEmpty(self):
        queue = JobQueue()
        jobs = [Job(None)]

        assert queue.is_empty()

        queue.add_jobs(jobs)

        assert not queue.is_empty()

    def testJobQueueLength(self):
        queue = JobQueue()
        jobs_1 = [Job(None)]
        jobs_2 = [Job(None)]

        queue.add_jobs(jobs_1)
        assert queue.get_length() == 1

        queue.add_jobs(jobs_2)
        assert queue.get_length() == 2

    def testJobPopsLessThanEntirety(self):
        queue = JobQueue()
        jobs = [Job(None)] * 10

        queue.add_jobs(jobs)
        assert len(queue.pop_jobs(5)) == 5

    def testJobPopsMoreThanEntirety(self):
        queue = JobQueue()
        jobs = [Job(None)] * 10

        queue.add_jobs(jobs)
        assert len(queue.pop_jobs(15)) == 10


if __name__ == '__main__':
    unittest.main()
