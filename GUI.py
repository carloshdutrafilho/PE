# GUI.py

from tkinter import Tk
from ttkthemes import ThemedStyle

class GUI:
    def __init__(self, master=None):
        self.master = Tk() if master is None else master
        self.master.geometry("800x600")  
        self.master.title("MedicAnalysis v1")
        self.style = ThemedStyle(self.master)
        self.style.set_theme("plastik")
