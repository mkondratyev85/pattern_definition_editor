import tkinter as tk

class SidePanel():
    def __init__(self, root):
        self.frame2 = tk.Frame(root)
        self.frame2.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.plotBut = tk.Button(self.frame2, text="Plot ")
        self.plotBut.pack(side="top", fill=tk.BOTH)
        self.clearButton = tk.Button(self.frame2, text="Clear")
        self.clearButton.pack(side="top", fill=tk.BOTH)
        self.SelectLIneButton = tk.Button(self.frame2, text="SelectLine")
        self.SelectLIneButton.pack(side="top", fill=tk.BOTH)
