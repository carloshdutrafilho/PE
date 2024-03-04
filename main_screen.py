# main_screen.py

from tkinter import *
from tkinter import Canvas, Frame, Label
from PIL import Image, ImageTk

class MainScreen(Frame):
    def __init__(self, master=None, app=None):
        super().__init__(master)
        self.app = app
        self.pack(expand=True, fill="both")

        self.msg = Label(self, text="Main Screen")
        self.msg["font"] = ("Verdana", "12", "bold")
        self.msg.pack()

        self.canvas = Canvas(self)
        self.canvas.pack(expand=True, fill="both")

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
            