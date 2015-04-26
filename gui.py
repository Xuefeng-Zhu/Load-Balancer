import toga

__author__ = 'Xuefeng Zhu'


class LoadBalance(toga.App):
    def startup(self):
        container = toga.Container()
        button = toga.Button('Hello world', on_press=self.button_handler)

        self.table = toga.Table(['Message'])

        container.add(button)

        container.constrain(button.TOP == container.TOP + 50)
        container.constrain(button.LEADING == container.LEADING + 50)
        container.constrain(button.TRAILING + 50 == container.TRAILING)
        container.constrain(button.BOTTOM + 50 < container.BOTTOM)

        split = toga.SplitContainer()

        split.content = [self.table, container]

        self.main_window.content = split

    def button_handler(self, _):
        self.table.insert(1, 'test')
        print "test"



app = LoadBalance('LoadBalance', 'cs423.load_balance')
app.main_loop()