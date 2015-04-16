__author__ = 'Dan'

import unittest

from HardwareMonitor import HardwareMonitor


class HardwareMonitorUsageTest(unittest.TestCase):
    def testHardwareMonitorTracksReasonableCpuUsage(self):
        monitor = HardwareMonitor()

        #cpu_usage = monitor.get_cpu_usage()
        #time.sleep(0.5)

        #assert cpu_usage > 0
        #assert cpu_usage < 10.0


if __name__ == '__main__':
    unittest.main()
