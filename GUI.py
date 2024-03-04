from tkinter import Tk

class GUI:
    def __init__(self, master=None):
        self.master = Tk() if master is None else master
        self.master.geometry("400x200")
        self.master.title("Image Loader")
