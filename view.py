import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from sidepanel import SidePanel

class View:
    def __init__(self, root, model):
        self.frame = tk.Frame(root)
        self.model = model
        self.fig = Figure(figsize=(7.5, 4), dpi=80)
        self.ax0 = self.fig.add_axes((0.05, .05, .90, .90), facecolor=(.75, .75, .75), frameon=False)
        self.frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.sidepanel = SidePanel(root)

        self.sidepanel.plotBut.bind("<Button>", self.plot)
        self.sidepanel.clearButton.bind("<Button>", self.clear)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.canvas.draw()

    def clear(self, event):
        self.ax0.clear()
        self.fig.canvas.draw()

    def plot(self, event):
        self.model.calculate()
        self.ax0.clear()
        self.ax0.contourf(self.model.res["x"], self.model.res["y"], self.model.res["z"])
        self.fig.canvas.draw()
