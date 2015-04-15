import math

__author__ = 'Dan'

import unittest

from Job import Job


class JobTestInitialize(unittest.TestCase):
    def testWorkDataInit(self):
        work_data = [1.111111, 1.111111, 1.111111, 1.111111, 1.111111]
        test_job = Job(work_data)

        assert test_job.work_data == work_data

    def testWorkDataInitAsNotFinished(self):
        work_data = [1.111111, 1.111111, 1.111111, 1.111111, 1.111111]
        test_job = Job(work_data)

        assert not test_job.is_finished()


class JobTestExecute(unittest.TestCase):
    def testJobExecuteOnce(self):
        work_data = [1.111111, 1.111111, 1.111111, 1.111111, 1.111111]
        test_job = Job(work_data)

        for i in range(1):
            test_job.execute_next()

        assert math.fabs(test_job.work_data[0] - 2.222222) < 1

    def testJobExecutesOnMoreThanOneElement(self):
        work_data = [1.111111, 1.111111, 1.111111, 1.111111, 1.111111]
        test_job = Job(work_data)

        for i in range(2000):
            test_job.execute_next()

        assert math.fabs(test_job.work_data[0] - 1001 * 1.111111) < 1
        assert math.fabs(test_job.work_data[1] - 1001 * 1.111111) < 1

    def testJobExecutesUntilFinish(self):
        work_data = [1.111111, 1.111111, 1.111111, 1.111111, 1.111111]
        test_job = Job(work_data)

        while not test_job.is_finished():
            test_job.execute_next()

        assert math.fabs(test_job.work_data[-1] - 1001 * 1.111111) < 1


if __name__ == '__main__':
    unittest.main()
