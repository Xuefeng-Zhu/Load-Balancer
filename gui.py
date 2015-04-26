import toga

__author__ = 'Xuefeng Zhu'


class LoadBalance(toga.App):
    def startup(self):
        self.table = toga.Table(['Message'])

        container = toga.Container()

        throttle_label = toga.Label('Throttling', alignment=toga.RIGHT_ALIGNED)
        throttle_button = toga.Button('Update', on_press=self.change_throttle)
        self.throttle_input = toga.TextInput()

        progress_label = toga.Label('Job Progress', alignment=toga.RIGHT_ALIGNED)
        self.progress_bar = toga.ProgressBar(1024, 0)

        container.add(throttle_label)
        container.add(throttle_button)
        container.add(self.throttle_input)

        container.add(progress_label)
        container.add(self.progress_bar)

        # throttle constrain
        container.constrain(throttle_label.TOP == container.TOP + 10)
        container.constrain(throttle_label.LEADING == container.LEADING + 10)

        container.constrain(self.throttle_input.WIDTH == 100)
        container.constrain(self.throttle_input.TOP == throttle_label.TOP)
        container.constrain(self.throttle_input.LEADING == throttle_label.TRAILING + 10)

        container.constrain(throttle_button.TOP == throttle_label.TOP)
        container.constrain(throttle_button.LEADING == self.throttle_input.TRAILING + 10)

        # job progress constrain
        container.constrain(progress_label.TOP == throttle_label.BOTTOM + 20)
        container.constrain(progress_label.LEADING == throttle_label.LEADING)

        container.constrain(self.progress_bar.WIDTH == 200)
        container.constrain(self.progress_bar.TOP == progress_label.TOP)
        container.constrain(self.progress_bar.LEADING == progress_label.TRAILING + 10)


        split = toga.SplitContainer()
        split.content = [self.table, container]
        self.main_window.content = split

    def change_throttle(self, _):
        self.table.insert(1, 'test')
        print "test"



app = LoadBalance('LoadBalance', 'cs423.load_balance')
app.main_loop()