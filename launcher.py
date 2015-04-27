import json
import sys
from time import sleep
from Queue import Queue
from job import Job
from worker_thread import WorkerThread
from hardware_monitor import HardwareMonitor
from state_manager import StateManager
from transfer_manager import TransferManager
from adaptor import Adaptor

__author__ = 'Xuefeng Zhu'

NUM_JOB = 1024
NUM_THREADS = 4


class Launcher:
    """
    The initiator of the whole program
    """

    def __init__(self, is_master, remote_ip, vector):
        self.is_master = is_master
        self.vector = vector
        self.finished_jobs = []

        self.job_queue = Queue()
        self.work_threads = []

        for i in range(NUM_THREADS):
            self.work_threads.append(WorkerThread(self.job_queue, self, i))

        self.hardware_monitor = HardwareMonitor(self.work_threads)
        self.transfer_manager = TransferManager(self.job_queue, remote_ip, self)
        self.state_manager = StateManager(remote_ip)
        self.adaptor = Adaptor(self.work_threads[0], self.job_queue,
                               self.transfer_manager, self.state_manager, self.hardware_monitor)

    def bootstrap(self):
        """
        Define the behavior for bootstrap phase
        """
        if self.is_master:
            self.allocate_jobs()
            self.transfer_jobs()

        self.hardware_monitor.start()
        self.transfer_manager.receive_job()
        self.state_manager.receive_state()
        self.state_manager.start()

        # wait until receiving half the job
        while self.job_queue.qsize() < NUM_JOB / 2:
            sleep(0.1)

        # receive all jobs and exit the bootstrap stage
        for i in range(NUM_THREADS):
            self.work_threads[i].start()

    def allocate_jobs(self):
        """
        Divide the vector into NUM_JOB jobs, and put jobs into job
        queue
        """
        job_size = len(self.vector) / NUM_JOB
        for i in range(NUM_JOB):
            pos = i * job_size
            job = Job(i, pos, self.vector[pos: pos + job_size])
            self.job_queue.put(job)

    def transfer_jobs(self):
        """
        Send half of jobs to slave node through transfer manager
        """
        for _ in range(NUM_JOB / 2):
            self.transfer_manager.send_job()

    def on_job_finish(self, job):
        """
        Callback function when a job finishes
        :param job: Job Object
        """

        # put the job into finished job if in master node
        # send the job to master node if in slave node
        if self.is_master:
            self.finished_jobs.append(job)
        else:
            self.transfer_manager.send_job(job)

        # start to aggregate jobs when all jobs finished
        if len(self.finished_jobs) == NUM_JOB:
            self.aggregate_jobs()

    def aggregate_jobs(self):
        """
        Map the data back to vector
        """
        for job in self.finished_jobs:
            pos = job.pos
            for data in job.work_data:
                self.vector[pos] = data
                pos += 1


def load_config():
    """
    Load the config information in config file
    """
    with open('config.json') as f:
        return json.load(f)


def print_data(vector):
    """
    Print value stored in the vector
    :param vector:
    """
    for i, v in enumerate(vector):
        print "A[%d]= %d" % (i, v)


if __name__ == '__main__':
    # instructor for running the program
    if len(sys.argv) != 2:
        print "Usage: python launcher.py M/S"
        exit(0)

    # Judge if master or slave
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

    for work_thread in launcher.work_threads:
        work_thread.join()

    # wait until all jobs finish
    while is_master and len(launcher.finished_jobs) != NUM_JOB:
        sleep(1)

    if is_master:
        print_data(vector)

    print "All jobs are finished!"
