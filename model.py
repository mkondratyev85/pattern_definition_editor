import math
from dataclasses import dataclass, field
from typing import Tuple, List, Optional
import pickle


class Model:

    def __init__(self):
        self.lines = [
                Line(base_point=(10, 10),
                     angle=30,
                     offset=(40, 2),
                     ),
                Line(base_point=(50, 50),
                     offset=(20, 20),
                     ),
                ]
    def add_new_line(self):
        self.lines.append(Line())

    def remove_line(self, line):
        self.lines.remove(line)

    def get_list_of_lines(self):
        l = []
        for line in self.lines:
            l.append(line.as_list())
        return l

    def from_list_to_lines(self, list_):
        self.lines = []
        for l in list_:
            line = Line(angle=l[0],
                        base_point=l[1],
                        offset=l[2],
                        dash_length_items=l[3],
                        )
            self.lines.append(line)
        


    def save_pattern(self, filename):
        lines = self.get_list_of_lines()
        with open(filename, 'wb') as f: pickle.dump(lines, f)

    def open_pattern(self, filename):
        with open(filename, 'rb') as f:
            lines = pickle.load(f)

        self.from_list_to_lines(lines)




@dataclass
class Line:
    '''
    Class for single line in pattern
    '''

    angle: float = 0
    base_point: Tuple[float, float] = (10, 10)
    offset: Tuple[float, float] = (10, 10)
    dash_length_items: list = field(default_factory=list)
    canvas_line_id: Optional[int] = None

    @property
    def length2nd(self) -> float:
        '''
        Returns length of solid segment in line
        (length to 2nd point)
        '''
        if self.dash_length_items:
            return self.dash_length_items[0]
        else:
            return 100

    @property
    def length3nd(self) -> float:
        '''
        Returns length of solid segment plus dashed segment in line
        (length to 3nd point)
        If line is solid - return length to second 
        '''
        if self.dash_length_items:
            return self.dash_length_items[0] - self.dash_length_items[1]
        else:
            return self.length2nd

    def add_dash(self) -> None:
        '''
        Adds dash element to the line.
        '''
        self.dash_length_items = [self.length2nd, -self.length2nd]

    @property
    def second_point(self) -> Tuple[float, float]:
        '''
        Returns second point from base_point
        '''
        x0, y0 = self.base_point
        x1 = x0 + self.length2nd * math.cos(math.radians(self.angle))
        y1 = y0 + self.length2nd * math.sin(math.radians(self.angle))
        return x1, y1

    @property
    def third_point(self) ->Optional[Tuple[float, float]]:
        '''
        Returns thrid point (representing dash).
        '''
        x0, y0 = self.base_point
        x2 = x0 + self.length3nd * math.cos(math.radians(self.angle))
        y2 = y0 + self.length3nd * math.sin(math.radians(self.angle))
        return x2, y2

    def update_2nd_point(self, x1: float, y1: float) -> None:
        '''
        Updates angle and dash_length_items based of 2nd point
        '''
        x0, y0 = self.base_point
        self.angle = math.degrees(math.atan2((y1 - y0), (x1 - x0)))
        if self.dash_length_items:
            length = math.sqrt((x1-x0)**2 + (y1-y0)**2)
            self.dash_length_items[0] = length

    def update_3nd_point(self, x1: float, y1: float) -> None:
        '''
        Updates dash_length_items based of 3nd point
        '''
        if self.dash_length_items:
            x0, y0 = self.base_point
            length = math.sqrt((x1-x0)**2 + (y1-y0)**2)
            length_ = length - self.dash_length_items[0]
            self.dash_length_items[1] = -length_


    def get_many_lines(self):
        '''
        Yields coordinates of lines that could be drawn from self
        '''

        for i in range(-15, 15, 1):
            x0, y0 = self.base_point
            dx, dy = self.offset
            x0 += i*dx
            y0 += i*dy
            new_line = Line(base_point=(x0, y0),
                            offset=self.offset,
                            angle=self.angle,
                            dash_length_items=self.dash_length_items,
                            )
            for j in range(-15, 15, 1):
                x0, y0 = new_line.base_point
                x1, y1 = new_line.third_point
                dx, dy = x1-x0, y1-y0
                x0 += j*dx
                y0 += j*dy
                new_new_line = Line(base_point=(x0, y0),
                                    offset=self.offset,
                                    angle=self.angle,
                                    dash_length_items=self.dash_length_items,
                                    )

                x0, y0 = new_new_line.base_point
                x1, y1 = new_new_line.second_point
                yield (x0, y0, x1, y1)

    def __hash__(self):
        return hash(str(self.base_point) + str(self.offset) + str(self.angle) + str(self.dash_length_items))

    def as_list(self):
        return [self.angle,
                self.base_point,
                self.offset,
                self.dash_length_items]


