import toga
import sys
from launcher import Launcher, load_config

__author__ = 'Xuefeng Zhu'


class LoadBalance(toga.App):
    def __init__(self, name, app_id):
        super(LoadBalance, self).__init__(name, app_id)

        self.launcher = None

        self.table = toga.Table(['Message'])
        self.throttle_input = toga.TextInput()
        self.progress_bar = toga.ProgressBar(1024, 0)

    def startup(self):
        container = toga.Container()

        throttle_label = toga.Label('Throttling', alignment=toga.RIGHT_ALIGNED)
        throttle_button = toga.Button('Update', on_press=self.change_throttle)

        progress_label = toga.Label('Job Progress', alignment=toga.RIGHT_ALIGNED)

        container.add(throttle_label)
        container.add(throttle_button)
        container.add(self.throttle_input)

        container.add(progress_label)
        container.add(self.progress_bar)

        # throttle constrain
        container.constrain(throttle_label.WIDTH == 100)
        container.constrain(throttle_label.TOP == container.TOP + 40)
        container.constrain(throttle_label.LEADING == container.LEADING + 10)

        container.constrain(self.throttle_input.WIDTH == 100)
        container.constrain(self.throttle_input.HEIGHT == 20)
        container.constrain(self.throttle_input.TOP == throttle_label.TOP)
        container.constrain(self.throttle_input.LEADING == throttle_label.TRAILING + 10)

        container.constrain(throttle_button.TOP == throttle_label.TOP)
        container.constrain(throttle_button.LEADING == self.throttle_input.TRAILING + 10)

        # job progress constrain
        container.constrain(progress_label.WIDTH == throttle_label.WIDTH)
        container.constrain(progress_label.TOP == throttle_label.BOTTOM + 20)
        container.constrain(progress_label.LEADING == throttle_label.LEADING)

        container.constrain(self.progress_bar.WIDTH == 200)
        container.constrain(self.progress_bar.HEIGHT == 20)
        container.constrain(self.progress_bar.TOP == progress_label.TOP)
        container.constrain(self.progress_bar.LEADING == progress_label.TRAILING + 10)


        split = toga.SplitContainer()
        split.content = [self.table, container]
        self.main_window.content = split

    def change_throttle(self, _):
        value = int(self.throttle_input.value)
        if value > 0:
            self.launcher.hardware_monitor.throttle(value)
            toga.Dialog.info('Success', 'Throttle value has been updated!')
        else:
            toga.Dialog.info('Error', 'Throttle input is invalid!')

    def on_message(self, message):
        self.table.insert(None, message)

    def on_job_finish(self):
        self.progress_bar.value += 1


if __name__ == '__main__':
    # instructor for running the program
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

    gui = LoadBalance('LoadBalance', 'cs423.load_balance')

    launcher = Launcher(is_master, remote_ip, gui)
    launcher.bootstrap()

    gui.launcher = launcher
    gui.main_loop()
