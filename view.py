import tkinter as tk
from tkinter import filedialog
import math

from sidepanel import SidePanel

DEFAULT = 0
MOVE_BASE_POINT = 1
MOVE_SECOND_POINT = 2
MOVE_OFFSET_POINT = 3
MOVE_THIRD_POINT = 4

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
        self.sidepanel.SelectLIneButton.bind("<Button>", self._switch_line_selection_on)
        self.sidepanel.AddLIneButton.bind("<Button>", self._add_new_line)
        self.sidepanel.RemoveLIneButton.bind("<Button>", self._remove_selected_line)
        self.sidepanel.SaveButton.bind("<Button>", self._save)
        self.sidepanel.OpenButton.bind("<Button>", self._open)
        self.sidepanel.AddDashButton.bind('<Button>', self._add_dash)

        self.angle_var = tk.StringVar()
        self.sidepanel.AngleEntry.config(textvariable=self.angle_var)
        self.base_point_var = tk.StringVar()
        self.sidepanel.BasePointEntry.config(textvariable=self.base_point_var)
        self.offset_var = tk.StringVar()
        self.sidepanel.OffsetEntry.config(textvariable=self.offset_var)
        self.dash_var = tk.StringVar()
        self.sidepanel.DashEntry.config(textvariable=self.dash_var)

        # self.angle_var.trace("w", self._angle_var_callback)
        # self.base_point_var.trace("w", self._base_point_var_callback)
        # self.offset_var.trace("w", self._offset_var_callback)
        self.sidepanel.AngleEntry.bind("<KeyRelease>", self._angle_var_callback)
        self.sidepanel.BasePointEntry.bind("<KeyRelease>", self._base_point_var_callback)
        self.sidepanel.OffsetEntry.bind("<KeyRelease>", self._offset_var_callback)
        self.sidepanel.DashEntry.bind("<KeyRelease>", self._dash_var_callback)

        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.canvas.bind('<ButtonPress-1>', self.on_line_click)
        self.canvas.bind('<ButtonRelease-1>', self.on_line_release)
        self.canvas.bind('<B1-Motion>', self.on_motion)

        self.selected_line_id = None
        self.do_select_lines = False

        self.draw_lines(None)

    def _angle_var_callback(self, *args):
        val = self.angle_var.get()
        line = self.get_line_by_object_id(self.selected_line_id)
        try:
            line.angle = float(val)
            self.redraw_line(self.selected_line_id)
        except ValueError:
            pass
            # self.angle_var.set(line.angle)

    def _base_point_var_callback(self, *args):
        val = self.base_point_var.get()
        line = self.get_line_by_object_id(self.selected_line_id)
        try:
            val = val[1:-2] # remove square braces
            val = val.split(',')
            x = float(val[0])
            y = float(val[1])
            line.base_point = x, y
            self.redraw_line(self.selected_line_id)
        except ValueError:
            pass
            # self.angle_var.set(f'{line.base_point}')

    def _offset_var_callback(self, *args):
        val = self.offset_var.get()
        line = self.get_line_by_object_id(self.selected_line_id)
        try:
            val = val[1:-2] # remove square braces
            val = val.split(',')
            dx = float(val[0])
            dy = float(val[1])
            line.offset = dx, dy
            self.redraw_line(self.selected_line_id)
        except ValueError:
            pass
            # self.angle_var.set(f'{line.base_point}')

    def _dash_var_callback(self, *args):
        val = self.dash_var.get()
        line = self.get_line_by_object_id(self.selected_line_id)
        try:
            val = val[1:-2] # remove square braces
            val = val.split(',')
            d0 = float(val[0])
            d1 = float(val[1])
            line.dash_length_items = [d0, d1]
            self.redraw_line(self.selected_line_id)
        except ValueError:
            pass
            # self.angle_var.set(f'{line.base_point}')

    def _add_dash(self, event):
        line = self.get_line_by_object_id(self.selected_line_id)
        line.add_dash()
        self.redraw_line(self.selected_line_id)

    def _open(self, event):
        filename = filedialog.askopenfile(mode='r', defaultextension='.pickle')
        if filename is None:
            return
        self.model.open_pattern(filename.name)
        self.draw_lines(None)
    
    def _save(self, event):
        filename = filedialog.asksaveasfile(mode='w', defaultextension='.pickle')
        if filename is None:
            return
        self.model.save_pattern(filename.name)

    def _add_new_line(self, event):
        self.model.add_new_line()
        self.draw_lines(event)

    def _remove_selected_line(self, event):
        line = self.get_line_by_object_id(self.selected_line_id)
        self.model.remove_line(line)
        self.draw_lines(event)

    def _switch_line_selection_on(self, event):
        self.do_select_lines = True


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
        elif self.mode == MOVE_THIRD_POINT:
            line.update_3nd_point(x, y)

        self.redraw_line(self.selected_line_id)

    def on_line_click(self, event):
        x, y = event.x, event.y
        SNAP_TOLERANCE = 5
        clicked_object_ids = event.widget.find_overlapping(x-SNAP_TOLERANCE, y-SNAP_TOLERANCE, x+SNAP_TOLERANCE, y+SNAP_TOLERANCE)
        if self.do_select_lines:
            line = self.get_line_by_object_id(clicked_object_ids[0])
            if line:
                self.selected_line_id = clicked_object_ids[0]
                self.redraw_line(clicked_object_ids[0])
                self.do_select_lines = False
        elif self.base_point_anchor_id in clicked_object_ids:
            self.mode = MOVE_BASE_POINT
        elif self.second_point_anchor_id in clicked_object_ids:
            self.mode = MOVE_SECOND_POINT
        elif self.offset_point_anchor_id in clicked_object_ids:
            self.mode = MOVE_OFFSET_POINT
        elif self.third_point_anchor_id in clicked_object_ids:
            self.mode = MOVE_THIRD_POINT
        
    def _update_entries(self):
        line = self.get_line_by_object_id(self.selected_line_id)
        self.angle_var.set(line.angle)
        self.base_point_var.set(f'{line.base_point}')
        self.offset_var.set(f'{line.offset}')
        self.dash_var.set(f'{line.dash_length_items}')

    def draw_lines(self, event):
        self.canvas.delete('all')
        for line in self.model.lines:
            line.canvas_line_id = []
            for coords in line.get_many_lines():
                id = self.canvas.create_line(*coords)
                line.canvas_line_id.append(id)

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
        self._update_entries()

    def draw_anchors(self, line_id, new=False):
        RW = 5  # width of point
        line = self.get_line_by_object_id(line_id)
        x0, y0 = line.base_point
        x1, y1 = line.second_point
        dx, dy = line.offset
        xo, yo = x0+dx, y0+dy
        x3, y3 = line.third_point
        base_coords = (x0-RW, y0-RW, x0+RW, y0+RW)
        second_coords = (x1-2*RW, y1-RW, x1+2*RW, y1+RW)
        offset_coords = (xo-RW, yo-RW, xo+RW, yo+RW)
        if line.dash_length_items:
            third_coords = (x3-RW, y3-RW, x3+RW, y3+RW)
        else:
            # in case we have a solid line we shift third point far beyond screen
            third_coords = -10,-10,-10,-10
        if new:
            id = self.canvas.create_rectangle(*base_coords)
            self.base_point_anchor_id = id
            id = self.canvas.create_rectangle(*second_coords)
            self.second_point_anchor_id = id
            id = self.canvas.create_rectangle(*offset_coords)
            self.offset_point_anchor_id = id
            id = self.canvas.create_rectangle(*third_coords)
            self.third_point_anchor_id = id
        else:
            self.canvas.coords(self.base_point_anchor_id, base_coords)
            self.canvas.coords(self.second_point_anchor_id, second_coords)
            self.canvas.coords(self.offset_point_anchor_id, offset_coords)
            self.canvas.coords(self.third_point_anchor_id, third_coords)



