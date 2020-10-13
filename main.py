import tkinter as tk
from tkinter import ttk

from view import View
from model import Model


class Controller:
    def __init__(self):
        self.root = tk.Tk()
        self.model = Model()
        self.view = View(self.root, self.model)

    def run(self):
        # self.root.geometry('400x250+300+300')
        self.root.mainloop()


def main() -> None:
    controller = Controller()
    controller.run()


if __name__ == '__main__':
    main()
