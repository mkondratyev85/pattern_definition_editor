import tkinter as tk
import math
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.figure import Figure

from sidepanel import SidePanel

class View:
    def __init__(self, root, model):
        self.model = model
        self.frame = tk.Frame(root)
        self.frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.canvas = tk.Canvas(self.frame)

        self.sidepanel = SidePanel(root)
        self.sidepanel.plotBut.bind("<Button>", self.plot)
        self.sidepanel.clearButton.bind("<Button>", self.clear)

        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def clear(self, event):
        self.canvas.delete('all')

    def on_line_click(self, event):
        print(event)
        cliecked_object_id = event.widget.find_closest(event.x, event.y)[0]
        print(cliecked_object_id)
        line = next(filter(lambda x: x.canvas_line_id == cliecked_object_id, self.model.lines), None)
        print(line)

    def plot(self, event):
        RW=5  # width of point
        self.canvas.delete('all')
        for line in self.model.lines:
            print(line)
            x0, y0 = line.base_point
            x1 = x0 + 100 * math.cos(math.radians(line.angle))
            y1 = y0 + 100 * math.sin(math.radians(line.angle))

            # draw line
            line_id = self.canvas.create_line(x0, y0, x1, y1)
            line.canvas_line_id = line_id
            # print(type(line))

            self.canvas.bind('<ButtonPress-1>', self.on_line_click)

            # draw base_point
            # self.canvas.create_rectangle(x0-RW, y0-RW, x0+RW, y0+RW)


