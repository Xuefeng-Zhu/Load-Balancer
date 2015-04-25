import math

__author__ = 'Dan'

import unittest

from job import Job


class JobInitializeTest(unittest.TestCase):
    def testWorkDataInit(self):
        work_data = [1.111111] * 5
        test_job = Job(0, 0, work_data)

        assert test_job.work_data == work_data

    def testWorkDataInitAsNotFinished(self):
        work_data = [1.111111] * 5
        test_job = Job(0, 0, work_data)

        assert not test_job.is_finished()


class JobExecuteTest(unittest.TestCase):
    def testJobExecuteOnce(self):
        work_data = [1.111111] * 5
        test_job = Job(0, 0, work_data)

        test_job.execute_next()

        self.assertEqual(int(test_job.work_data[0]), 1112)

    def testJobExecutesOnMoreThanOneElement(self):
        work_data = [1.111111] * 5
        test_job = Job(0, 0, work_data)

        for i in range(2000):
            test_job.execute_next()

        self.assertEqual(int(test_job.work_data[0]), 1112)
        self.assertEqual(int(test_job.work_data[1]), 1112)

    def testJobExecutesUntilFinish(self):
        work_data = [1.111111] * 5
        test_job = Job(0, 0, work_data)

        while not test_job.is_finished():
            test_job.execute_next()

        self.assertEqual(int(test_job.work_data[-1]), 1112)


if __name__ == '__main__':
    unittest.main()
