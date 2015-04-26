import socket
import pickle
import zlib
from functools import wraps
from threading import Thread

__author__ = 'Xuefeng Zhu'

HOST = ''
PORT = 12346


def thread_func(func):
    """
    Decorator function for launching thread
    """

    @wraps(func)
    def start_thread(*args, **kwargs):
        thread = Thread(target=func, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()
        return thread

    return start_thread


class TransferManager:
    """
    Manager responsible for sending and receiving jobs from another node
    """

    def __init__(self, job_queue, remote_ip, launcher):
        self.job_queue = job_queue
        self.remote_ip = remote_ip
        self.launcher = launcher

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((HOST, PORT))

    @thread_func
    def send_job(self, job):
        """
        Send job to another node
        """
        job_p = pickle.dumps(job)

        # compress data
        data = zlib.compress(job_p)
        self.socket.sendto(data, (self.remote_ip, PORT))

        print "Job %d sent" % job.id

    @thread_func
    def send_job(self, num_jobs):
        """
        Send jobs to another node
        """
        for _ in range(num_jobs):
            job = self.job_queue.get()
            job_p = pickle.dumps(job)

            # compress data
            data = zlib.compress(job_p)
            self.socket.sendto(data, (self.remote_ip, PORT))

            print "Job %d sent" % job.id

    @thread_func
    def receive_job(self):
        """
        Receive job from another node
        """
        while True:
            data, _ = self.socket.recvfrom(8192)

            # decompress data
            job_p = zlib.decompress(data)
            job = pickle.loads(job_p)

            # check if job has been finished
            if job.is_finished():
                self.launcher.on_job_finish(job)
            else:
                self.job_queue.put(job)

            print "Job %d received" % job.id

