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
        
        # Initialize image_paths attribute
        self.image_paths = []
        
        # Slider for scrolling through images/Time
        self.image_slider = ttk.Scale(self, from_=0, to=len(self.image_paths)-1, variable=self.current_time, orient=tk.HORIZONTAL, command=self.update_image_slider)
        self.image_slider.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Add entry widgets for parameters
        self.moyennage_label = tk.Label(self, text="Temp. averaging=")
        self.moyennage_label.pack(side=tk.LEFT, padx=5, pady=10)
        self.moyennage_entry = tk.Entry(self, width=10)
        self.moyennage_entry.pack(side=tk.LEFT, padx=10, pady=10)
        self.moyennage_entry.bind("<Return>", self.temporal_averaging)

        # Contrast adjustment
        self.contrast_label = tk.Label(self, text="Contrast=")
        self.contrast_label.pack(side=tk.LEFT, padx=5, pady=10)
        self.contrast_slider = ttk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, command=self.update_contrast)
        self.contrast_slider.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Brightness adjustment
        self.brightness_label = tk.Label(self, text="Brightness=")
        self.brightness_label.pack(side=tk.LEFT, padx=5, pady=10)
        self.brightness_slider = ttk.Scale(self, from_=-100, to=100, orient=tk.HORIZONTAL, command=self.update_brightness)
        self.brightness_slider.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Label to display current brightness value
        #self.brightness_value_label = tk.Label(self, text="Brightness: 0      ", bd=1, relief=tk.SOLID)
        #self.brightness_value_label.place(x=0, y=0)  # Initial position
        #self.brightness_value_label.pack_forget()  # Hide initially 13
        
        # Labels to display contrast, threshold_min, and threshold_max
        #self.contrast_value_label = tk.Label(self, text="Contrast: 0          ", bd=1, relief=tk.SOLID)
        #self.contrast_value_label.place(x=0, y=20)
        #self.contrast_value_label.pack_forget()

        #self.threshold_min_value_label = tk.Label(self, text="Threshold Min: 0", bd=1, relief=tk.SOLID)
        #self.threshold_min_value_label.place(x=0, y=40)
        #self.threshold_min_value_label.pack_forget()

        #self.threshold_max_value_label = tk.Label(self, text="Threshold Max: 0", bd=1, relief=tk.SOLID)
        #self.threshold_max_value_label.place(x=0, y=60)
        #self.threshold_max_value_label.pack_forget()
        
        # Label to display current parameters
        self.parameters_label = tk.Label(self, text="Contrast: 0\nBrightness: 0\nThreshold Min: 0\nThreshold Max: 0  ", bd=1, relief=tk.SOLID, width=20, height=4)
        self.parameters_label.place(x=0, y=0)  # Initial position
        self.parameters_label.pack_forget()  # Hide initially
        
        # Threshold adjustment
        self.threshold_min_label = tk.Label(self, text="Min Threshold=")
        self.threshold_min_label.pack(side=tk.LEFT, padx=5, pady=10)
        self.threshold_min_slider = ttk.Scale(self, from_=0, to=1, orient=tk.HORIZONTAL, command=self.update_threshold)
        self.threshold_min_slider.pack(side=tk.LEFT, padx=10, pady=10)

        self.threshold_max_label = tk.Label(self, text="Max Threshold=")
        self.threshold_max_label.pack(side=tk.LEFT, padx=5, pady=10)
        self.threshold_max_slider = ttk.Scale(self, from_=0, to=1, orient=tk.HORIZONTAL, command=self.update_threshold)
        self.threshold_max_slider.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Color change button
        self.color_change_button = tk.Button(self, text="Change Color", command=self.change_color)
        self.color_change_button.pack(side=tk.TOP, anchor=tk.NE, padx=10, pady=10)
        
        # Temporal averaging variables
        self.window_size = 1  # Initial window size
        self.images_for_temporal_averaging = []  # List to store images for averaging
                
        # Keep a reference to the original image for reset functionality
        self.original_image = None
        self.image = None
        self.color_mode = 'grayscale'  # Initial color mode
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
        contrast = round(self.contrast_slider.get() / 100.0, 2)  # Round to two decimal places

        # Update the contrast label with the current value
        #self.contrast_value_label.config(text=f"Contrast: {contrast}")
        
        # Update the parameters label with the current values
        self.update_parameters_label(contrast=contrast)
        
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
        brightness = round(self.brightness_slider.get(), 2)  # Round to two decimal places
        
        # Update the brightness label with the current value
        #self.brightness_value_label.config(text=f"Brightness: {brightness}")

        # Update the parameters label with the current values
        self.update_parameters_label(brightness=brightness)
        
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
            
    def update_window_size(self):
        # Get the window size for temporal averaging from the entry widget
        window_size = int(self.moyennage_entry.get())

        # Check if the window size is valid
        if window_size < 1 or window_size > len(self.image_paths):
            return

        # Update the window size and reload images for temporal averaging
        self.window_size = window_size
        self.load_images_for_temporal_averaging()

            
    def load_images_for_temporal_averaging(self):
        # Load the images within the specified window for temporal averaging
        start_time = int(self.current_time.get())
        end_time = min(start_time + self.window_size, len(self.image_paths))

        images_to_average = [np.array(Image.open(self.image_paths[i])) for i in range(start_time, end_time)]
        images_to_average = np.array(images_to_average) / 255.0  # Normalize pixel values to [0, 1]

        # Update the list of images for temporal averaging
        self.images_for_temporal_averaging = images_to_average

        # Perform temporal averaging and update the displayed image
        self.temporal_averaging()

    def temporal_averaging(self, event=None):
        # Check if there are images for temporal averaging
        if not self.images_for_temporal_averaging:
            return

        # Perform temporal averaging
        averaged_image = np.mean(self.images_for_temporal_averaging, axis=0)

        # Update the displayed image using Matplotlib
        self.axis.imshow(averaged_image, cmap='gray')
        self.canvas.draw_idle()
            
    def update_threshold(self, *args):
        # Get threshold values from the sliders
        threshold_min = round(self.threshold_min_slider.get(), 2)  # Round to two decimal places
        threshold_max = round(self.threshold_max_slider.get(), 2)  # Round to two decimal places
        
        # Update the threshold labels with the current values
        #self.threshold_min_value_label.config(text=f"Threshold Min: {threshold_min}")
        #self.threshold_max_value_label.config(text=f"Threshold Max: {threshold_max}")

        # Update the parameters label with the current values
        self.update_parameters_label(threshold_min=threshold_min, threshold_max=threshold_max)

        # Apply threshold adjustment
        thresholded_image = self.threshold(self.image, threshold_min, threshold_max)

        # Update the displayed image using Matplotlib
        self.axis.imshow(thresholded_image, cmap='gray')
        self.canvas.draw_idle()

    def threshold(self, image, threshold_min, threshold_max):
        # Apply minimum and maximum thresholds to images
        thresholded_image = np.copy(image)
        thresholded_image[image < threshold_min] = 0  # Set values below the min threshold to 0
        thresholded_image[image > threshold_max] = 1  # Set values above the max threshold to 0
        
        return thresholded_image 
    
    def update_parameters_label(self, brightness=None, contrast=None, threshold_min=None, threshold_max=None):
        # Get the current label text
        current_text = self.parameters_label.cget("text")

        # Extract the previously set values from the current label text
        previous_brightness = current_text.split("\n")[0].split(": ")[1]
        previous_contrast = current_text.split("\n")[1].split(": ")[1]
        previous_threshold_min = current_text.split("\n")[2].split(": ")[1]
        previous_threshold_max = current_text.split("\n")[3].split(": ")[1]

        # Set the values to the previous values if they are None
        brightness = previous_brightness if brightness is None else brightness
        contrast = previous_contrast if contrast is None else contrast
        threshold_min = previous_threshold_min if threshold_min is None else threshold_min
        threshold_max = previous_threshold_max if threshold_max is None else threshold_max

        # Update the parameters label with the current values
        parameters_text = f"Contrast: {contrast}\nBrightness: {brightness}\nThreshold Min: {threshold_min}\nThreshold Max: {threshold_max}  "
        self.parameters_label.config(text=parameters_text)
    
    def update_displayed_image(self):
        # Update the displayed image using Matplotlib
        if self.color_mode == 'inverted':
            displayed_image = 1 - self.image
        else:
            displayed_image = self.image

        self.axis.imshow(displayed_image, cmap='gray')
        self.canvas.draw_idle()

    def change_color(self):
        # Change the color mode between 'grayscale' and 'inverted'
        self.color_mode = 'inverted' if self.color_mode == 'grayscale' else 'grayscale'
        self.update_displayed_image()
           