import Tkinter as tk
import ttk
from Tkinter import *
import tkMessageBox
import sys
from threading import Thread, Lock
from launcher import Launcher, load_config

__author__ = 'Yanwen and Xuefeng'


class LoadBalance(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.launcher = None
        self.is_start = False
        self.lock = Lock()

        style = ttk.Style()
        style.configure("BW.TLabel", foreground="black", background="white")
        self.start_button = ttk.Button(text="Start", command=self.start_launcher)
        self.start_button.pack()

        self.label = ttk.Label(text="Enter the Throttling Value:", style="BW.TLabel")
        self.label.pack()
        self.entry = ttk.Entry(self)
        self.entry.pack()
        self.button = ttk.Button(text="change", command=self.change_throttle)
        self.button.pack()

        self.progress_label = ttk.Label(text="Job Progress:", style="BW.TLabel")
        self.progress = ttk.Progressbar(self, orient="horizontal",
                                        length=200, mode="determinate")
        self.progress["maximum"] = 1024
        self.progress["value"] = 0
        self.progress.pack()

        self.jobs_label = ttk.Label(text="Pending Jobs: 0", style="BW.TLabel")
        self.jobs_label.pack()
        self.throttling_label = ttk.Label(text="Throttling: 100", style="BW.TLabel")
        self.throttling_label.pack()
        self.cpu_label = ttk.Label(text="CPU Usage: 0", style="BW.TLabel")
        self.cpu_label.pack()

        self.mess_label = ttk.Label(text="Message:", style="BW.TLabel")
        self.mess_label.pack()
        self.table = Listbox()
        self.table.pack()

    def start_launcher(self):
        if not self.is_start:
            self.is_start = True
            thread = Thread(target=self.launcher.bootstrap)
            thread.start()

    def change_throttle(self):
        value = int(self.entry.get())
        if value > 0:
            self.launcher.hardware_monitor.throttle(value)
            tkMessageBox.showinfo('Success', 'Throttle value has been updated!')
        else:
            tkMessageBox.showinfo('Error', 'Throttle input is invalid!')

    def on_state_update(self, state):
        self.jobs_label.configure(text="Pending Jobs: %d" %state.num_jobs)
        self.throttling_label.configure(text="Throttling: %d" %state.throttling)
        self.cpu_label.configure(text="CPU Usage: %d" %state.cpu_usage)

    def on_job_finish(self):
        self.lock.acquire()
        self.progress["value"] += 1
        self.lock.release()

    def on_message(self, message):
        self.table.insert(0, message)


if __name__ == '__main__':
    # instruction for running the program
    if len(sys.argv) != 2:
        print "Usage: python gui.py M/S"
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

    else:
        remote_ip = config["master"]

    gui = LoadBalance()
    launcher = Launcher(is_master, remote_ip, gui)
    gui.launcher = launcher

    gui.mainloop()
