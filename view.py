import tkinter as tk
import math

from sidepanel import SidePanel

DEFAULT = 0
MOVE_BASE_POINT = 1
MOVE_SECOND_POINT = 2
MOVE_OFFSET_POINT = 3

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

        if self.mode == MOVE_BASE_POINT:
            line.base_point = x, y
        elif self.mode == MOVE_SECOND_POINT:
            line.update_2nd_point(x, y)
        elif self.mode == MOVE_OFFSET_POINT:
            x0, y0 = line.base_point
            line.offset = (x-x0, y-y0)

        self.redraw_line(self.selected_line_id)

    def on_line_click(self, event):
        clicked_object_id = event.widget.find_closest(event.x, event.y)[0]
        line = self.get_line_by_object_id(clicked_object_id)
        if line:
            self.selected_line_id = clicked_object_id
            self.redraw_line(clicked_object_id)
        elif clicked_object_id == self.base_point_anchor_id:
            self.mode = MOVE_BASE_POINT
        elif clicked_object_id == self.second_point_anchor_id:
            self.mode = MOVE_SECOND_POINT
        elif clicked_object_id == self.offset_point_anchor_id:
            self.mode = MOVE_OFFSET_POINT
        

    def draw_lines(self, event):
        self.canvas.delete('all')
        for line in self.model.lines:

            line.canvas_line_id = []
            for coords in line.get_many_lines():
                canvas_line_id = self.canvas.create_line(*coords)
                line.canvas_line_id.append(canvas_line_id)

        first_line_id = self.model.lines[0].canvas_line_id[0]
        self.selected_line_id = first_line_id
        self.redraw_line(first_line_id, new=True)

    def get_line_by_object_id(self, canvas_object_id):
        for line in self.model.lines:
            if canvas_object_id in line.canvas_line_id:
                return line

    def redraw_line(self, line_id, new=False):
        line = self.get_line_by_object_id(line_id)
        canvas_line_ids = line.canvas_line_id
        for id, coords in zip(line.canvas_line_id, line.get_many_lines()):
            self.canvas.coords(id, coords)
        self.draw_anchors(line_id, new)

    def draw_anchors(self, line_id, new=False):
        RW = 5  # width of point
        line = self.get_line_by_object_id(line_id)
        x0, y0 = line.base_point
        x1, y1 = line.second_point
        dx, dy = line.offset
        xo, yo = x0+dx, y0+dy
        base_coords = (x0-RW, y0-RW, x0+RW, y0+RW)
        second_coords = (x1-2*RW, y1-RW, x1+2*RW, y1+RW)
        offset_coords = (xo-RW, yo-RW, xo+RW, yo+RW)
        if new:
            id = self.canvas.create_rectangle(*base_coords)
            self.base_point_anchor_id = id
            id = self.canvas.create_rectangle(*second_coords)
            self.second_point_anchor_id = id
            id = self.canvas.create_rectangle(*offset_coords)
            self.offset_point_anchor_id = id
        else:
            self.canvas.coords(self.base_point_anchor_id, base_coords)
            self.canvas.coords(self.second_point_anchor_id, second_coords)
            self.canvas.coords(self.offset_point_anchor_id, offset_coords)



