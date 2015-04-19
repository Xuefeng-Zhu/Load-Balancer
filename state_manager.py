import socket
import pickle
from functools import wraps
from threading import Thread
from time import sleep

__author__ = 'Xuefeng Zhu'

HOST = ''
PORT = 12345


def thread_func(func):
    @wraps(func)
    def start_thread(*args, **kwargs):
        thread = Thread(target=func, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()
        return thread

    return start_thread


class StateManager:
    def __init__(self, adaptor, remote_ip):
        self.adaptor = adaptor
        self.remote_ip = remote_ip

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((HOST, PORT))

    @thread_func
    def send_state(self, state):
        state_p = pickle.dumps(state)

        self.socket.sendto(state_p, (self.remote_ip, PORT))

        print "Local state sent"

    @thread_func
    def receive_state(self):
        while True:
            state_p, _ = self.socket.recvfrom(2048)
            state = pickle.loads(state_p)
            self.adaptor.on_state_receive(state)

            print "Remote state received"

    @thread_func
    def start(self):
        while True:
            state = self.adaptor.on_state_send()
            self.send_state(state)

            sleep(30)



