from tkinter import *
from tkinter import Canvas, Frame, Label
from PIL import Image, ImageTk

# ...

class MainScreen(Frame):
    def __init__(self, master=None, app=None):
        super().__init__(master)
        self.app = app  
        self.pack(expand=True, fill="both")

        self.msg = Label(self, text="Main Screen")
        self.msg["font"] = ("Verdana", "12", "bold")
        self.msg.pack()

        # Adicione um Canvas para exibir a imagem
        self.canvas = Canvas(self, width=300, height=200)
        self.canvas.pack()

    def display_image(self, image_path):
        img = Image.open(image_path)

        img = img.resize((300, 200), Image.ANTIALIAS) if hasattr(Image, 'ANTIALIAS') else img.resize((300, 200))

        img_tk = ImageTk.PhotoImage(img)

        self.canvas.create_image(150, 100, anchor=CENTER, image=img_tk)

        self.canvas.image = img_tk

