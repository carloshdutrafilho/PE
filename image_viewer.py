import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

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
        
        # Initialize image_paths attribute
        self.image_paths = []
        
        # Slider for scrolling through images/Time
        self.image_slider = ttk.Scale(self, from_=0, to=len(self.image_paths)-1, variable=self.current_time, orient=tk.HORIZONTAL, command=self.update_image_slider)
        self.image_slider.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Add entry widgets for parameters
        self.moyennage_label = tk.Label(self, text="Temp. averaging:")
        self.moyennage_label.pack(side=tk.LEFT, padx=5, pady=10)
        self.moyennage_entry = tk.Entry(self, width=10)
        self.moyennage_entry.pack(side=tk.LEFT, padx=10, pady=10)
        self.moyennage_entry.bind("<Return>", self.temporal_averaging)

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
    
        self.image = self.normalized_image_array.copy()  # Create a copy for editing
        self.original_photo = ImageTk.PhotoImage(self.original_image)
        self.axis.imshow(self.image, cmap='gray')
        self.canvas.draw_idle()

    def update_time_slider(self, max_time):
        self.time_slider.configure(to=max_time)
        
    def get_parameters(self):
        # Get parameter values
        moyennage = int(self.moyennage_entry.get())
        contrast = self.contrast_slider.get()
        return moyennage, contrast
    
    def update_contrast(self, *args):
        # Get contrast value from the slider
        contrast = self.contrast_slider.get() / 100.0  # Normalize to range [-1, 1]

        # Apply contrast adjustment
        contrasted_image = self.contrast(self.image, contrast)

        # Update the displayed image using Matplotlib
        self.axis.imshow(contrasted_image, cmap='gray')
        self.canvas.draw_idle()

    def contrast(self, image, value_contrast):
        # Calculate the contrasted image by multiplying by the contrast value
        image_contrasted = np.clip(image * (1.0 + value_contrast), 0, 1)  # Normalize to [0, 1]

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
        print("Selected Time:", selected_time)
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
            
    def temporal_averaging(self, event=None):
        # Get the window size for temporal averaging from the entry widget
        window_size = int(self.moyennage_entry.get())

        # Check if the window size is valid
        if window_size < 1 or window_size > len(self.image_paths):
            return

        # Load the images within the specified window for temporal averaging
        start_time = int(self.current_time.get())
        end_time = min(start_time + window_size, len(self.image_paths))

        images_to_average = [np.array(Image.open(self.image_paths[i])) for i in range(start_time, end_time)]
        images_to_average = np.array(images_to_average) / 255.0  # Normalize pixel values to [0, 1]

        # Perform temporal averaging
        averaged_image = np.mean(images_to_average, axis=0)

        # Update the displayed image using Matplotlib
        self.axis.imshow(averaged_image, cmap='gray')
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