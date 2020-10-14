import tkinter as tk
import math

from sidepanel import SidePanel

DEFAULT = 0
MOVE_BASE_POINT = 1

class View:
    def __init__(self, root, model):
        self.mode = DEFAULT
        self.model = model
        self.frame = tk.Frame(root)
        self.frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.canvas = tk.Canvas(self.frame)

        self.sidepanel = SidePanel(root)
        self.sidepanel.plotBut.bind("<Button>", self.draw_lines)
        self.sidepanel.clearButton.bind("<Button>", self.clear)

        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.canvas.bind('<ButtonPress-1>', self.on_line_click)
        self.canvas.bind('<ButtonRelease-1>', self.on_line_release)
        self.canvas.bind('<B1-Motion>', self.on_motion)

        self.selected_line_id = None

    def clear(self, event):
        self.canvas.delete('all')

    def on_line_release(self, event):
        self.mode = DEFAULT

    def on_motion(self, event):
        if self.mode == DEFAULT:
            return
        x, y = event.x, event.y
        line = self.get_line_by_object_id(self.selected_line_id)
        line.base_point = x, y
        self.draw_anchors(self.selected_line_id)
        self.redraw_line(self.selected_line_id)
        print('motion')

    def on_line_click(self, event):
        clicked_object_id = event.widget.find_closest(event.x, event.y)[0]
        line = self.get_line_by_object_id(clicked_object_id)
        if line:
            self.selected_line_id = clicked_object_id
            self.draw_anchors(clicked_object_id)
            print(line)
        if clicked_object_id == self.base_point_anchor_id:
            print('ya')
            self.mode = MOVE_BASE_POINT
        

    def draw_lines(self, event):
        self.canvas.delete('all')
        for line in self.model.lines:
            x0, y0 = line.base_point
            x1, y1 = line.second_point

            line_id = self.canvas.create_line(x0, y0, x1, y1)
            line.canvas_line_id = line_id

        first_line_id = self.model.lines[0].canvas_line_id
        self.selected_line_id = first_line_id
        self.draw_anchors(first_line_id, new=True)

    def get_line_by_object_id(self, canvas_object_id):
        line = next(filter(lambda x: x.canvas_line_id == canvas_object_id, self.model.lines), None)
        return line

    def redraw_line(self, line_id):
        line = self.get_line_by_object_id(line_id)
        x0, y0 = line.base_point
        x1, y1 = line.second_point
        coords = (x0, y0, x1, y1)
        self.canvas.coords(line_id, coords)

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



