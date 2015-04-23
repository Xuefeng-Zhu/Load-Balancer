from state import State

__author__ = 'Xuefeng'

JOB_QUEUE_LIMIT = 200


class Adaptor:
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
        self.local_state.num_jobs = self.job_queue.qsize()
        self.local_state.throttling = self.work_thread.throttling
        self.local_state.cpu_usage = self.hardware_monitor.get_cpu_usage()

    def on_state_send(self):
        self.update_local_state()
        return self.local_state

    def on_state_receive(self, state):
        self.remote_state = state
        self.on_state_update()

    def on_state_update(self):
        if self.job_queue.qsize() > JOB_QUEUE_LIMIT:
            if self.remote_state.num_jobs < JOB_QUEUE_LIMIT:
                num_transfer_jobs = min(self.job_queue.qsize()-JOB_QUEUE_LIMIT,
                                        JOB_QUEUE_LIMIT-self.remote_state.num_jobs)
                for _ in range(num_transfer_jobs):
                    self.transfer_manager.send_job()




