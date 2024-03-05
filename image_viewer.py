import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

class ImageViewer(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.current_time = tk.DoubleVar()
        self.current_time.set(0)

        self.image_label = tk.Label(self)
        self.image_label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.time_slider = ttk.Scale(self, from_=0, to=10, variable=self.current_time, orient=tk.HORIZONTAL)
        self.time_slider.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Add entry widgets for parameters
        self.moyennage_entry = tk.Entry(self, width=10)
        self.moyennage_entry.pack(side=tk.LEFT, padx=10, pady=10)
        self.moyennage_label = tk.Label(self, text="Moyennage:")
        self.moyennage_label.pack(side=tk.LEFT, padx=5, pady=10)

        self.contrast_slider = ttk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL)
        self.contrast_slider.pack(side=tk.LEFT, padx=10, pady=10)
        self.contrast_label = tk.Label(self, text="Contrast:")
        self.contrast_label.pack(side=tk.LEFT, padx=5, pady=10)

    def load_image(self, image_path):
        # Load and display image
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)
        self.image_label.configure(image=photo)
        self.image_label.image = photo

    def update_time_slider(self, max_time):
        self.time_slider.configure(to=max_time)
        
    def get_parameters(self):
        # Get parameter values
        moyennage = self.moyennage_entry.get()
        contrast = self.contrast_slider.get()
        return moyennage, contrast
