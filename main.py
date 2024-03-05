# main.py
from tkinter import Tk
from GUI import GUI
from load_screen import LoadScreen
from main_screen import MainScreen

class Application:
    def __init__(self, master=None):
        self.master = master
        self.gui = GUI(master)

        self.selected_file = None

        self.load_screen = LoadScreen(self.master, app=self)
        self.load_screen.b_load.config(command=self.load_screen.load_image)

        self.main_screen = MainScreen(self.master, app=self)
        self.main_screen.pack_forget()

    def show_main_screen(self):
        if self.selected_file:
            self.load_screen.pack_forget()
            self.main_screen.pack(expand=True, fill="both")
            self.main_screen.display_image(self.selected_file)
            
            

if __name__ == "__main__":
    root = Tk()
    app = Application(master=root)
    app.master.mainloop()