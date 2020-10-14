import tkinter as tk

class SidePanel():
    def __init__(self, root):
        self.frame2 = tk.Frame(root)
        self.frame2.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.plotBut = tk.Button(self.frame2, text="Plot ")
        self.plotBut.pack(side="top", fill=tk.BOTH)
        self.clearButton = tk.Button(self.frame2, text="Clear")
        self.clearButton.pack(side="top", fill=tk.BOTH)
        self.SelectLIneButton = tk.Button(self.frame2, text="Select Line")
        self.SelectLIneButton.pack(side="top", fill=tk.BOTH)
        self.AddLIneButton = tk.Button(self.frame2, text="Add Line")
        self.AddLIneButton.pack(side="top", fill=tk.BOTH)
        self.RemoveLIneButton = tk.Button(self.frame2, text="Remove Selected Line")
        self.RemoveLIneButton.pack(side="top", fill=tk.BOTH)
        self.SaveButton = tk.Button(self.frame2, text="Save Pattern")
        self.SaveButton.pack(side="top", fill=tk.BOTH)
