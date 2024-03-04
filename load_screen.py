from tkinter import Frame, Label, Button
from tkinter import filedialog
import os

class LoadScreen(Frame):
    def __init__(self, master=None, app=None):
        super().__init__(master)
        self.app = app
        self.pack(expand=True, fill="both")

        self.msg = Label(self, text="Create your project")
        self.msg["font"] = ("Verdana", "12", "bold")
        self.msg.pack()

        self.b_load = Button(self, text="Load image", font=("Calibri", "10"), width=15, command=self.load_image)
        self.b_load.pack()

    def load_image(self):
        current_folder = os.path.dirname(os.path.abspath(__file__))
        file_path = filedialog.askopenfilename(title="Select Image File", initialdir=current_folder, filetypes=[(".tiff files", "*.tiff")])

        if file_path:
            # If a file is selected, show the main screen
            self.app.selected_file = file_path
            self.app.show_main_screen()
