from tkinter import Frame, Label

class MainScreen(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(expand=True, fill="both")

        self.msg = Label(self, text="Main Screen")
        self.msg["font"] = ("Verdana", "12", "bold")
        self.msg.pack()
