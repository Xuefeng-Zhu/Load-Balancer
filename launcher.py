from Queue import Queue
from job import Job
from worker_thread import WorkerThread
from hardware_monitor import HardwareMonitor
from state_manager import StateManager
from transfer_manager import TransferManager
from adaptor import Adaptor

__author__ = 'Xuefeng Zhu'

NUM_JOB = 1024


class Launcher:
    def __init__(self, remote_ip):
        self.job_queue = Queue()
        self.work_thread = WorkerThread(self.job_queue)
        self.hardware_monitor = HardwareMonitor(self.work_thread)
        self.transfer_manager = TransferManager(self.job_queue, remote_ip)
        self.state_manager = StateManager(remote_ip)
        self.adaptor = Adaptor(self.work_thread, self.job_queue,
                               self.transfer_manager, self.state_manager, self.hardware_monitor)

    def bootstrap(self):
        self.hardware_monitor.start()
        self.transfer_manager.receive_job()
        self.state_manager.receive_state()

    def allocate_jobs(self, vector):

        job_size = len(vector) / NUM_JOB
        for i in range(NUM_JOB):
            pos = i * job_size
            job = Job(pos, vector[pos, pos + job_size])
            self.job_queue.put(job)

    def transfer_jobs(self):
        for i in range(NUM_JOB/2):
            job = self.job_queue.get()
            self.transfer_manager.send_job(job)


if __name__ == '__main__':
    vector = [1.111111] * 1024 * 1024 * 32
    remote_ip = "1.1.1.1"

    launcher = Launcher(remote_ip)
    launcher.allocate_jobs(vector)
    launcher.transfer_jobs()
    launcher.bootstrap()

    launcher.work_thread.join()
