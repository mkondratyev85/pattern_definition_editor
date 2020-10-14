import math
from dataclasses import dataclass, field
from typing import Tuple, List, Optional


class Model:

    def __init__(self):
        self.xpoint = 200
        self.ypoint = 200
        self.res = None
        self.lines = [
                Line(base_point=(10,10),
                     angle=30,
                     ),
                Line(base_point=(50,50)),
                ]


    def calculate(self):
        pass
        # x, y = np.meshgrid(np.linspace(-5, 5, self.xpoint), np.linspace(-5, 5, self.ypoint))
        # z = np.cos(x ** 2 * y ** 3)
        # self.res = {"x": x, "y": y, "z": z}


@dataclass
class Line:
    '''
    Class for single line in pattern
    '''

    angle: float = 0
    base_point: Tuple[float, float] = (0, 0)
    offset: Tuple[float, float] = (0, 0)
    dash_length_items: list = field(default_factory=list)
    canvas_line_id: Optional[int] = None

    @property
    def length(self) -> float:
        '''
        Returns length of solid segment in line
        '''
        return 100

    @property
    def second_point(self) -> Tuple[float, float]:
        '''
        Returns second point from base_point
        '''
        x0, y0 = self.base_point
        x1 = x0 + self.length * math.cos(math.radians(self.angle))
        y1 = y0 + self.length * math.sin(math.radians(self.angle))
        return x1, y1
