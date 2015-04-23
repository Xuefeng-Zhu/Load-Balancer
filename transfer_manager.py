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
    def __init__(self, job_queue, remote_ip, launcher):
        self.job_queue = job_queue
        self.remote_ip = remote_ip
        self.launcher = launcher

        self.send_socket = socket.socket()
	self.send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.recv_socket = socket.socket()
        self.recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.recv_socket.bind((HOST, PORT))
        self.recv_socket.listen(5)

    @thread_func
    def send_job(self, job_list):
        self.send_socket.connect((self.remote_ip, PORT))

        job_list_p = pickle.dumps(job_list)
        self.send_socket.sendall(job_list_p)

        for job in job_list:
            print "Job %d sent" % job.id

    @thread_func
    def receive_job(self):
        while True:
            client, _ = self.recv_socket.accept()
            data = []
            while True:
                tmp = client.recv(4096)
                if tmp:
                    data.append(tmp)
                else:
                    break

            job_list = pickle.loads(''.join(data))
            print str(job_list)
            for job in job_list:
                if job.is_finished():
                    self.launcher.on_job_finish(job)
                else:
                    self.job_queue.put(job)

                print "Job %d received" % job.id

            client.close()
