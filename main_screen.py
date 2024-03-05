# main_screen.py

from tkinter import *
from tkinter import Canvas, Frame, Label
from PIL import Image, ImageTk
from data_viewer import DataViewer
from image_viewer import ImageViewer

class MainScreen(Frame):
    def __init__(self, master=None, app=None):
        super().__init__(master)
        self.app = app
        self.pack(expand=True, fill="both")

        self.msg = Label(self, text="Main Screen")
        self.msg["font"] = ("Verdana", "12", "bold")
        self.msg.pack()

        # Container for DataViewer and ImageViewer
        main_container = Frame(self)
        main_container.pack(side=TOP, fill=BOTH, expand=True)

        self.data_viewer = DataViewer(main_container)
        self.data_viewer.pack(side=LEFT, fill=BOTH, expand=False)

        self.image_viewer = ImageViewer(main_container)
        self.image_viewer.pack(side=LEFT, fill=BOTH, expand=True)

        # GraphFrame (You may customize or add additional containers as needed)
        self.graph_frame = Frame(self)  
        self.graph_frame.pack(side=TOP, fill=BOTH, expand=True)

    def display_image(self, image_path):
        try:
            img = Image.open(image_path)

            window_width = self.winfo_reqwidth()
            window_height = self.winfo_reqheight()

            # img = img.resize((window_width, window_height), Image.NEAREST)  # Use NEAREST for no antialiasing

            img_tk = ImageTk.PhotoImage(img)

            self.canvas.config(width=window_width, height=window_height)
            self.canvas.create_image(window_width // 2, window_height // 2, anchor=CENTER, image=img_tk)
            self.canvas.image = img_tk

            self.img_tk = img_tk
        except Exception as e:
            print(f"Erro ao exibir imagem: {e}")
            