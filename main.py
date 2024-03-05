# main.py
from tkinter import Tk
from GUI import GUI
from load_screen import LoadScreen
from main_screen import MainScreen

class Application:
    def __init__(self, master=None):
        self.master = master
        self.gui = GUI()

        self.selected_file = None

        self.load_screen = LoadScreen(self.master, app=self)
        self.load_screen.b_load_image.config(command=self.load_screen.load_image)

        self.main_screen = MainScreen(self.master, app=self)
        self.main_screen.pack_forget()

    def show_main_screen(self):
        if self.selected_file:
            self.load_screen.pack_forget()
            self.main_screen.pack(expand=True, fill="both")
            self.main_screen.display_image(self.selected_file)

            # Update the time slider with the maximum time
            max_time = 10  # Replace with your actual max time
            self.gui.image_viewer.update_time_slider(max_time)

            # Add code for displaying data and creating graphs
            # (You need to integrate this with your specific implementation)

            # Call methods from old_gui to integrate image_viewer and data_viewer
            self.gui.image_viewer.show_image(self.selected_file)
            self.gui.data_viewer.display_data()  # Add your data display code here

if __name__ == "__main__":
    root = Tk()
    app = Application(master=root)
    app.master.mainloop()
