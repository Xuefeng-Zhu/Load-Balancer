import socket
import pickle
import zlib
from functools import wraps
from threading import Thread
from time import sleep

__author__ = 'Xuefeng Zhu'

HOST = ''
PORT = 12346


def thread_func(func):
    @wraps(func)
    def start_thread(*args, **kwargs):
        thread = Thread(target=func, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()
        return thread

    return start_thread


class TransferManager:
    def __init__(self, job_queue, remote_ip, launcher):
        self.job_queue = job_queue
        self.remote_ip = remote_ip
        self.launcher = launcher

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((HOST, PORT))

    @thread_func
    def send_job(self, job=None):
        if job is None:
            job = self.job_queue.get()
        job_p = pickle.dumps(job)
        data = zlib.compress(job_p)
        self.socket.sendto(data, (self.remote_ip, PORT))

        print "Job %d sent" % job.id

    @thread_func
    def receive_job(self):
        while True:
            data, _ = self.socket.recvfrom(8192)
            job_p = zlib.decompress(data)
            job = pickle.loads(job_p)
            if job.is_finished():
                self.launcher.on_job_finish(job)
            else:
                self.job_queue.put(job)

            print "Job %d received" % job.id

