import tkinter as tk
from tkinter import filedialog

class FileViewer(tk.Frame):
    def __init__(self, master=None, image_viewer=None):
        super().__init__(master, bg='white')

        self.image_viewer = image_viewer

        self.file_path_var = tk.StringVar()
        self.file_path_label = tk.Label(self, textvariable=self.file_path_var, bg='white')
        self.file_path_label.pack(pady=10)

        open_file_button = tk.Button(self, text="Open File", command=self.open_file)
        open_file_button.pack(pady=10)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("TIFF files", "*.tiff;*.tif")])
        if file_path:
            self.file_path_var.set(file_path)
            self.image_viewer.load_image(file_path)

    def clear_file_path(self):
        self.file_path_var.set("")
