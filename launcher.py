import json
import sys
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
    def __init__(self, is_master, remote_ip, vector):
        self.is_local = is_master
        self.vector = vector
        self.finished_jobs = []

        self.job_queue = Queue()
        self.work_thread = WorkerThread(self.job_queue, self)
        self.hardware_monitor = HardwareMonitor(self.work_thread)
        self.transfer_manager = TransferManager(self.job_queue, remote_ip, self)
        self.state_manager = StateManager(remote_ip)
        self.adaptor = Adaptor(self.work_thread, self.job_queue,
                               self.transfer_manager, self.state_manager, self.hardware_monitor)

    def bootstrap(self):
        if self.is_master:
            self.allocate_jobs()
            self.transfer_jobs()

        self.hardware_monitor.start()
        self.transfer_manager.receive_job()
        self.state_manager.receive_state()
        self.state_manager.start()

    def allocate_jobs(self):

        job_size = len(self.vector) / NUM_JOB
        for i in range(NUM_JOB):
            pos = i * job_size
            job = Job(i, pos, self.vector[pos, pos + job_size])
            self.job_queue.put(job)

    def transfer_jobs(self):
        for _ in range(NUM_JOB / 2):
            job = self.job_queue.get()
            self.transfer_manager.send_job(job)

    def on_job_finish(self, job):
        if self.is_local:
            self.finished_jobs.append(job)
        else:
            self.transfer_jobs(job)

        if len(self.finished_jobs) == NUM_JOB:
            self.aggregate_jobs()

    def aggregate_jobs(self):
        for job in self.finished_jobs:
            pos = job.pos
            for data in job.work_data:
                self.vector[pos] = data
                pos += 1


def load_config():
    with open('config.json') as f:
        return json.load(f)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: python launcher.py M/S"
        exit(0)

    if sys.argv[1] == "M":
        is_master = True
    elif sys.argv[1] == "S":
        is_master = False
    else:
        print "Please provide valid argument"
        exit(0)

    config = load_config()
    if is_master:
        remote_ip = config["slave"]
        vector = [1.111111] * 1024 * 1024 * 32
    else:
        remote_ip = config["master"]
        vector = None

    launcher = Launcher(is_master, remote_ip, vector)
    launcher.bootstrap()

    launcher.work_thread.join()
