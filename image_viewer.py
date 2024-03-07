import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from PIL import ImageSequence

class ImageViewer(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.current_time = tk.DoubleVar()
        self.current_time.set(0)
        
        # Placeholder image
        self.placeholder_image = Image.new("RGB", (500, 450), "lightgray")
        self.placeholder_photo = ImageTk.PhotoImage(self.placeholder_image)

        # Create a Matplotlib figure and axis for image display
        self.figure = Figure(figsize=(6, 6))
        self.axis = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        
        # Image label with the placeholder image
        #self.image_label = tk.Label(self, image=self.placeholder_photo)
        #self.image_label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        #self.time_slider = ttk.Scale(self, from_=0, to=10, variable=self.current_time, orient=tk.HORIZONTAL)
        #self.time_slider.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Additional slider for scrolling through images
        self.image_slider = ttk.Scale(self, from_=0, to=10, variable=self.current_time, orient=tk.HORIZONTAL, command=self.update_image_slider)
        self.image_slider.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Initialize image_paths attribute
        self.image_paths = []
        
        # Add entry widgets for parameters
        self.moyennage_label = tk.Label(self, text="Temp. averaging:")
        self.moyennage_label.pack(side=tk.LEFT, padx=5, pady=10)
        self.moyennage_entry = tk.Entry(self, width=10)
        self.moyennage_entry.pack(side=tk.LEFT, padx=10, pady=10)

        # Contrast adjustment
        self.contrast_label = tk.Label(self, text="Contrast:")
        self.contrast_label.pack(side=tk.LEFT, padx=5, pady=10)
        self.contrast_slider = ttk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, command=self.update_contrast)
        self.contrast_slider.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Brightness adjustment
        self.brightness_label = tk.Label(self, text="Brightness:")
        self.brightness_label.pack(side=tk.LEFT, padx=5, pady=10)
        self.brightness_slider = ttk.Scale(self, from_=-100, to=100, orient=tk.HORIZONTAL, command=self.update_brightness)
        self.brightness_slider.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Threshold adjustment
        self.threshold_min_label = tk.Label(self, text="Min Threshold:")
        self.threshold_min_label.pack(side=tk.LEFT, padx=5, pady=10)
        self.threshold_min_slider = ttk.Scale(self, from_=0, to=1, orient=tk.HORIZONTAL, command=self.update_threshold)
        self.threshold_min_slider.pack(side=tk.LEFT, padx=10, pady=10)

        self.threshold_max_label = tk.Label(self, text="Max Threshold:")
        self.threshold_max_label.pack(side=tk.LEFT, padx=5, pady=10)
        self.threshold_max_slider = ttk.Scale(self, from_=0, to=1, orient=tk.HORIZONTAL, command=self.update_threshold)
        self.threshold_max_slider.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Keep a reference to the original image for reset functionality
        self.original_image = None
        self.image = None
        self.reset_image()

    def load_image(self, image_path):
        # Load and display image using Matplotlib
        self.original_image = Image.open(image_path)

        # Convert the original image to a NumPy array
        self.original_image_array = np.array(self.original_image)

        ##
        # Normalize the pixel values to the range [0, 1]
        min_value = np.min(self.original_image_array)
        max_value = np.max(self.original_image_array)
        self.normalized_image_array = (self.original_image_array - min_value) / (max_value - min_value)
        ##
    
        self.image = self.normalized_image_array[int(self.current_time.get())].copy()  # Create a copy for editing
        self.original_photo = ImageTk.PhotoImage(self.original_image)
        self.axis.imshow(self.image, cmap='gray')
        self.canvas.draw_idle()
        self.canvas.draw()

    # def load_image(self, image_path):
    # # Open the TIFF file
    #     tiff_image = Image.open(image_path)

    #     # Create a list to store the images from different pages
    #     image_pages = []

    #     # Iterate over all pages in the TIFF file
    #     for page in ImageSequence.Iterator(tiff_image):
    #         # Convert the page to a NumPy array
    #         page_array = np.array(page)

    #         # Normalize the pixel values to the range [0, 1]
    #         min_value = np.min(page_array)
    #         max_value = np.max(page_array)
    #         normalized_page_array = (page_array - min_value) / (max_value - min_value)

    #         # Append the normalized page array to the list
    #         image_pages.append(normalized_page_array)

    #     # Set the current image based on the current_time variable
    #     current_time_index = int(self.current_time.get())
    #     if current_time_index < 0 or current_time_index >= len(image_pages):
    #         return  # Handle the case when the specified time is out of bounds

    #     self.image = image_pages[current_time_index].copy()  # Use the selected time index
    #     self.original_photo = ImageTk.PhotoImage(tiff_image)
    #     self.axis.imshow(self.image, cmap='gray')
    #     self.canvas.draw_idle()
    #     self.canvas.draw()

    def update_time_slider(self, max_time):
        self.time_slider.configure(to=max_time)
        
    def get_parameters(self):
        # Get parameter values
        moyennage = int(self.moyennage_entry.get())
        contrast = self.contrast_slider.get()
        return moyennage, contrast
    
    def update_contrast(self, *args):
        # Get contrast value from the slider
        contrast = int(self.contrast_slider.get())

        # Apply contrast adjustment
        contrasted_image = self.contrast(self.image, contrast)

        # Update the displayed image
        #contrasted_photo = ImageTk.PhotoImage(contrasted_image)
        #self.image_label.configure(image=contrasted_photo)
        #self.image_label.image = contrasted_photo
        # Update the displayed image using Matplotlib
        self.axis.imshow(contrasted_image, cmap='gray')
        self.canvas.draw_idle()

    def contrast(self, image, value_contrast):
        # Calculate the contrasted image by multiplying by the contrast value
        image_contrasted = np.clip(image * value_contrast / 100, 0, 1)  # Normalize to [0, 1]

        return image_contrasted
    
    def update_brightness(self, *args):
        # Get brightness value from the slider
        brightness = self.brightness_slider.get()

        # Apply brightness adjustment
        brightened_image = self.brightness(self.image, brightness)

        # Update the displayed image using Matplotlib
        self.axis.imshow(brightened_image, cmap='gray')
        self.canvas.draw_idle()

    def brightness(self, image, brightness_value):
    
        # Calculate the image with adjusted brightness by adding the brightness value
        image_brightened = np.clip(image + brightness_value / 255, 0, 1)  # Normalize to [0, 1]
        
        # Print debug information
        print("Original Image Array:")
        print(self.normalized_image_array)
        print("Brightness Value:", brightness_value)
        
        # Print the adjusted image array
        print("Brightened Image Array:")
        print(image_brightened)
        
        return image_brightened
    
    def load_image_at_time(self, time):
        if not self.image_paths:
            return  # No images loaded yet

        if time < 0 or time >= len(self.image_paths):
            return  # Handle the case when the specified time is out of bounds

        selected_image_path = self.image_paths[time]
        self.load_image(selected_image_path)
        
    def update_image_slider(self, *args):
        # You can implement logic here to handle scrolling through images
        # Example: Load the image at the selected time point
        selected_time = int(self.current_time.get())
        # Load the image based on the selected time
        # Call the appropriate method to load the image at the selected time
        self.load_image_at_time(selected_time)
    
    def reset_image(self):
        # Reset the image to its original state
        if self.original_image:
            self.image = self.normalized_image_array.copy()
            self.image_slider.set(0)
            self.contrast_slider.set(0)  # Update the contrast slider
            self.brightness_slider.set(0)  # Update the brightness slider
            self.threshold_min_slider.set(0)  # Update the min threshold slider
            self.threshold_max_slider.set(1)  # Update the max threshold slider
            self.axis.clear()
            self.axis.imshow(self.image, cmap='gray')
            self.canvas.draw_idle()
            
    def update_threshold(self, *args):
        # Get threshold values from the sliders
        threshold_min = self.threshold_min_slider.get()
        threshold_max = self.threshold_max_slider.get()

        # Apply threshold adjustment
        thresholded_image = self.threshold(self.image, threshold_min, threshold_max)

        # Update the displayed image using Matplotlib
        self.axis.imshow(thresholded_image, cmap='gray')
        self.canvas.draw_idle()

    def threshold(self, image, threshold_min, threshold_max):
        # Apply minimum and maximum thresholds to images
        thresholded_image = np.copy(image)
        thresholded_image[image < threshold_min] = 0  # Set values below the min threshold to 0
        thresholded_image[image > threshold_max] = 0  # Set values above the max threshold to 0
        thresholded_image[(image >= threshold_min) & (image <= threshold_max)] = 1  # Set values within the range to 1

        return thresholded_image        
    
