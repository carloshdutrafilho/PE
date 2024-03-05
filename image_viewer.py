import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import numpy as np

class ImageViewer(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.current_time = tk.DoubleVar()
        self.current_time.set(0)
        
        # Placeholder image
        self.placeholder_image = Image.new("RGB", (300, 200), "lightgray")
        self.placeholder_photo = ImageTk.PhotoImage(self.placeholder_image)

        # Image label with the placeholder image
        self.image_label = tk.Label(self, image=self.placeholder_photo)
        self.image_label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.time_slider = ttk.Scale(self, from_=0, to=10, variable=self.current_time, orient=tk.HORIZONTAL)
        self.time_slider.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Add entry widgets for parameters
        self.moyennage_entry = tk.Entry(self, width=10)
        self.moyennage_entry.pack(side=tk.LEFT, padx=10, pady=10)
        self.moyennage_label = tk.Label(self, text="Moyennage:")
        self.moyennage_label.pack(side=tk.LEFT, padx=5, pady=10)

        # Contrast adjustment
        self.contrast_slider = ttk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, command=self.update_contrast)
        self.contrast_slider.pack(side=tk.LEFT, padx=10, pady=10)
        self.contrast_label = tk.Label(self, text="Contrast:")
        self.contrast_label.pack(side=tk.LEFT, padx=5, pady=10)
        
        # Brightness adjustment
        self.brightness_slider = ttk.Scale(self, from_=-100, to=100, orient=tk.HORIZONTAL, command=self.update_brightness)
        self.brightness_slider.pack(side=tk.LEFT, padx=10, pady=10)
        self.brightness_label = tk.Label(self, text="Brightness:")
        self.brightness_label.pack(side=tk.LEFT, padx=5, pady=10)

    def load_image(self, image_path):
        # Load and display image
        self.image = Image.open(image_path)
        self.original_photo = ImageTk.PhotoImage(self.image)
        self.image_label.configure(image=self.original_photo)
        self.image_label.image = self.original_photo

    def update_time_slider(self, max_time):
        self.time_slider.configure(to=max_time)
        
    def get_parameters(self):
        # Get parameter values
        moyennage = self.moyennage_entry.get()
        contrast = self.contrast_slider.get()
        return moyennage, contrast
    
    def update_contrast(self, *args):
        # Get contrast value from the slider
        contrast = int(self.contrast_slider.get())

        # Apply contrast adjustment
        contrasted_image = self.contrast(self.image, contrast)

        # Update the displayed image
        contrasted_photo = ImageTk.PhotoImage(contrasted_image)
        self.image_label.configure(image=contrasted_photo)
        self.image_label.image = contrasted_photo

    def contrast(self, image, value_contrast):
        # Calculate the contrasted image by multiplying by the contrast value
        image_contrasted = np.clip(image * value_contrast / 100, 0, 255).astype(np.uint8)
        return Image.fromarray(image_contrasted)
    
    def update_brightness(self, *args):
        # Get brightness value from the slider
        brightness = int(self.brightness_slider.get())

        # Apply brightness adjustment
        brightened_image = self.brightness(self.image, brightness)

        # Update the displayed image
        brightened_photo = ImageTk.PhotoImage(brightened_image)
        self.image_label.configure(image=brightened_photo)
        self.image_label.image = brightened_photo

    def brightness(self, image, brightness_value):
        # Calculate the image with adjusted brightness by adding the brightness value
        image_brightened = np.clip(image + brightness_value, 0, 255).astype(np.uint8)
        return Image.fromarray(image_brightened)
