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
        self.sidepanel.plotBut.bind("<Button>", self.draw_lines)
        self.sidepanel.clearButton.bind("<Button>", self.clear)

        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def clear(self, event):
        self.canvas.delete('all')

    def on_line_click(self, event):
        clicked_object_id = event.widget.find_closest(event.x, event.y)[0]
        line = self.get_line_by_object_id(clicked_object_id)
        self.draw_anchors(clicked_object_id)
        print(line)

    def draw_lines(self, event):
        self.canvas.delete('all')
        for line in self.model.lines:
            x0, y0 = line.base_point
            x1, y1 = line.second_point

            # draw line
            line_id = self.canvas.create_line(x0, y0, x1, y1)
            line.canvas_line_id = line_id
            # print(type(line))

            self.canvas.bind('<ButtonPress-1>', self.on_line_click)

            # draw base_point
            # self.canvas.create_rectangle(x0-RW, y0-RW, x0+RW, y0+RW)
        self.draw_anchors(self.model.lines[0].canvas_line_id, new=True)

    def get_line_by_object_id(self, canvas_object_id):
        line = next(filter(lambda x: x.canvas_line_id == canvas_object_id, self.model.lines), None)
        return line

    def draw_anchors(self, line_id, new=False):
        RW=5  # width of point
        line = self.get_line_by_object_id(line_id)
        x0, y0 = line.base_point
        x1, y1 = line.second_point
        coords = (x0-RW, y0-RW, x0+RW, y0+RW)
        if new:
            id = self.canvas.create_rectangle(*coords)
            self.base_point_anchor_id = id
        else:
            self.canvas.coords(self.base_point_anchor_id, coords)



