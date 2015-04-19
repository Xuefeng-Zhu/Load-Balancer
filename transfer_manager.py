import socket
import pickle
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
    def __init__(self, job_queue ,remote_ip):
        self.job_queue = job_queue
        self.remote_ip = remote_ip

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((HOST, PORT))

    @thread_func
    def send_job(self):
        job = self.job_queue.get()
        job_p = pickle.dumps(job)

        self.socket.sendto(job_p, (self.remote_ip, PORT))

        print "Job sent"

    @thread_func
    def receive_job(self):
        while True:
            job_p, _ = self.socket.recvfrom(2048)
            job = pickle.loads(job_p)
            self.job_queue.put(job)

            print "Job received"

