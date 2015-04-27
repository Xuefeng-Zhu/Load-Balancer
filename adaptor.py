from state import State

__author__ = 'Xuefeng'

JOB_QUEUE_MAX = 200
JOB_QUEUE_MIN = 20
JOB_QUEUE_MAX_DIFF = 20


class Adaptor:
    """
    Adaptor works as a central hub to communicate between different componenet
    """

    def __init__(self, work_thread, job_queue, transfer_manager,
                 state_manager, hardware_monitor, gui):
        self.work_thread = work_thread
        self.job_queue = job_queue
        self.transfer_manager = transfer_manager
        self.state_manager = state_manager
        self.state_manager.adaptor = self
        self.hardware_monitor = hardware_monitor
        self.gui = gui

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
        if self.gui:
            self.gui.on_state_update(self.local_state)
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
        self.sender_init_throttle()

    def sender_init(self):
        """
        Initiate the transfer job based on local state
        """
        if self.job_queue.qsize() > JOB_QUEUE_MAX:
            if self.remote_state.num_jobs < JOB_QUEUE_MAX:
                num_transfer_jobs = min(self.job_queue.qsize() - JOB_QUEUE_MAX,
                                        JOB_QUEUE_MAX - self.remote_state.num_jobs)
                self.transfer_manager.send_jobs(num_transfer_jobs)

    def receiver_init(self):
        """
        Initiate the transfer job based on remote state
        """
        if self.remote_state.num_jobs < JOB_QUEUE_MIN:
            if self.job_queue.qsize() > JOB_QUEUE_MIN:
                num_transfer_jobs = min(self.job_queue.qsize() - JOB_QUEUE_MIN,
                                        JOB_QUEUE_MIN - self.remote_state.num_jobs)
                self.transfer_manager.send_jobs(num_transfer_jobs)

    def sender_init_throttle(self):
        """
        Initiate the transfer job based on remote state
        """
        update_amount = self.job_queue.qsize() - self.remote_state.num_jobs
        if update_amount > JOB_QUEUE_MAX_DIFF:
            num_transfer_jobs = update_amount * self.remote_state.throttling / self.local_state.throttling
            actual_transfer_jobs = min(num_transfer_jobs, self.job_queue.qsize())
            print "Load Balance: %d" % actual_transfer_jobs
            self.transfer_manager.send_jobs(actual_transfer_jobs)

    def symmetric_init(self):
        """
        Apply both sender and receiver init
        """
        self.sender_init()
        self.receiver_init()
