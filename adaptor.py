from state import State

__author__ = 'Xuefeng'

JOB_QUEUE_MAX = 200
JOB_QUEUE_MIN = 20


class Adaptor:
    """
    Adaptor works as a central hub to communicate between different componenet
    """

    def __init__(self, work_thread, job_queue, transfer_manager,
                 state_manager, hardware_monitor):
        self.work_thread = work_thread
        self.job_queue = job_queue
        self.transfer_manager = transfer_manager
        self.state_manager = state_manager
        self.state_manager.adaptor = self
        self.hardware_monitor = hardware_monitor

        self.remote_state = State()
        self.local_state = State()

    def update_local_state(self):
        """
        Update local state with lastest system statistics
        """
        self.local_state.num_jobs = self.job_queue.qsize()
        self.local_state.throttling = self.work_thread.throttling
        self.local_state.cpu_usage = self.hardware_monitor.get_cpu_usage()

    def on_state_send(self):
        """
        Callback function when state is going to be sent
        """
        self.update_local_state()
        return self.local_state

    def on_state_receive(self, state):
        """
        Callback function when remote state is received
        :param state: state Object
        """
        self.remote_state = state
        self.on_state_update()

    def on_state_update(self):
        """
        Callback funciton when remote state is update.
        This function also triggers the transfer policy
        """
        self.send_init()

    def sender_init(self):
        if self.job_queue.qsize() > JOB_QUEUE_MAX:
            if self.remote_state.num_jobs < JOB_QUEUE_MAX:
                num_transfer_jobs = min(self.job_queue.qsize() - JOB_QUEUE_MAX,
                                        JOB_QUEUE_MAX - self.remote_state.num_jobs)
                for _ in range(num_transfer_jobs):
                    self.transfer_manager.send_job()

    def receiver_init(self):
        if self.remote_state.num_jobs < JOB_QUEUE_MIN:
            if self.job_queue.qsize() > JOB_QUEUE_MIN:
                num_transfer_jobs = min(self.job_queue.qsize() - JOB_QUEUE_MIN,
                                        JOB_QUEUE_MIN - self.remote_state.num_jobs)
                for _ in range(num_transfer_jobs):
                    self.transfer_manager.send_job()