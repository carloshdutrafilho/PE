from GUI import GUI
from load_screen import LoadScreen
from main_screen import MainScreen
from tkinter import Tk

class Application:
    def __init__(self, master=None):
        self.master = master
        self.gui = GUI()

        self.load_screen = LoadScreen(self.gui)
        self.load_screen.b_load.config(command=self.show_main_screen)

        self.main_screen = MainScreen(self.gui)
        self.main_screen.pack_forget()

    def show_main_screen(self):
        self.load_screen.pack_forget()
        self.main_screen.pack()

if __name__ == "__main__":
    root = Tk()
    app = Application(root)
    root.mainloop()
