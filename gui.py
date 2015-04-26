from Tkinter import *
import numpy as np
import matplotlib

matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

__author__ = 'Yanwen'


class Application(Frame):
    ''' A GUI application that shows Job progress. '''

    # construction method
    def __init__(self, master):
        ''' Initialize the Frame '''
        Frame.__init__(self, master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        '''Create throttling widget'''
        Label(self,
              text="Enter the Throttling Value:"
        ).grid(row=0, column=0, columnspan=2, sticky=W)

        self.throttling = Entry(self)
        self.throttling.grid(row=1, column=0, sticky=W)

        Button(self,
               text="Change",
               command=self.update_throttling
        ).grid(row=2, column=0, sticky=W)

        self.text = Text(self, width=35, height=5, wrap=WORD)
        self.text.grid(row=3, column=0, sticky=W)

        '''Create progress bar'''
        Label(self,
              text="Job Progress ToolBar",
              font=("Helvetica", 20),
        ).grid(row=4, column=0, columnspan=2, sticky=W)

        '''Create state bar'''
        Label(self,
              text="State Progress ToolBar",
              font=("Helvetica", 20),
        ).grid(row=4, column=2, columnspan=2, sticky=W)

        '''Create message list'''
        Label(self,
              text="Message List",
              font=("Helvetica", 20),
        ).grid(row=6, column=0, columnspan=2, sticky=W)


    def update_throttling(self):
        '''Display throttling value '''
        content = self.throttling.get()

        #Need to put set throttling func here
        if True:
            message = "Success! Change throttling to " + content
        else:
            message = "Failure! Can't change throttling value."

        self.text.delete(0.0, END)
        self.text.insert(0.0, message)

        #this is a test func to show figs
        f = Figure()

        a = f.add_subplot(111)
        t = np.arange(0.0, 3.0, 0.01)
        s = np.sin(2 * np.pi * t)

        a.plot(t, s)

        a.set_title('Job Progress Graph')
        a.set_xlabel('X axis label')
        a.set_ylabel('Y label')

        # a tk.DrawingArea
        canvas = FigureCanvasTkAgg(f, master=root)
        canvas.get_tk_widget().grid(row=5, column=0)

        toolbar = NavigationToolbar2TkAgg(canvas, root)
        toolbar.grid(row=6, column=0)


root = Tk()
root.title("GUI")
root.geometry("800x1000")
app = Application(root)

root.mainloop()
