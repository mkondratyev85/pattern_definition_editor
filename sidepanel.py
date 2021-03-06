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
        self.AddDashButton = tk.Button(self.frame2, text="Add Dash to Line")
        self.AddDashButton.pack(side="top", fill=tk.BOTH)
        self.RemoveLIneButton = tk.Button(self.frame2, text="Remove Selected Line")
        self.RemoveLIneButton.pack(side="top", fill=tk.BOTH)

        tk.Label(self.frame2, text="Angle:").pack(side='top', fill=tk.BOTH)
        self.AngleEntry = tk.Entry(self.frame2)
        self.AngleEntry.pack(side='top', fill=tk.BOTH)
        tk.Label(self.frame2, text="Base Point:").pack(side='top', fill=tk.BOTH)
        self.BasePointEntry = tk.Entry(self.frame2)
        self.BasePointEntry.pack(side='top', fill=tk.BOTH)
        tk.Label(self.frame2, text="Offset:").pack(side='top', fill=tk.BOTH)
        self.OffsetEntry = tk.Entry(self.frame2)
        self.OffsetEntry.pack(side='top', fill=tk.BOTH)
        tk.Label(self.frame2, text="Dash:").pack(side='top', fill=tk.BOTH)
        self.DashEntry = tk.Entry(self.frame2)
        self.DashEntry.pack(side='top', fill=tk.BOTH)


        self.SaveButton = tk.Button(self.frame2, text="Save Pattern")
        self.SaveButton.pack(side="top", fill=tk.BOTH)
        self.OpenButton = tk.Button(self.frame2, text="Open Pattern")
        self.OpenButton.pack(side="top", fill=tk.BOTH)
