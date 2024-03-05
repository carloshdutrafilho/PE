# main.py
from tkinter import Tk
from GUI import GUI

class Application:
    def __init__(self, master=None):
        self.master = master
        self.gui = GUI()

        self.selected_file = None

if __name__ == "__main__":
    root = Tk()
    app = Application(master=root)
    app.master.mainloop()
