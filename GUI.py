from tkinter import Tk

class GUI(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("400x200")
        self.title("Medical Imaging Analysis v1")
