# main.py
import string
from tkinter import Tk
from GUI import GUI
from load_screen import LoadScreen
#from main_screen import MainScreen

class Application:
    def __init__(self, master=None):
        self.master = master
        self.gui = GUI()

        self.selected_file = None

    # def show_main_screen(self):
    #     if self.selected_file:
    #         self.load_screen.pack_forget()
    #         self.gui.pack(expand=True, fill="both")
    #         self.gui.display_image(self.selected_file)

    #         # Atualizar o controle deslizante de tempo com o tempo máximo
    #         max_time = 10  # Substitua pelo seu tempo máximo real
    #         self.gui.image_viewer.update_time_slider(max_time)

    #         self.gui.image_viewer.load_image(self.selected_file)  # Add your data display code here


if __name__ == "__main__":
    root = Tk()
    app = Application(master=root)
    #app.show_main_screen()
    app.master.mainloop()
