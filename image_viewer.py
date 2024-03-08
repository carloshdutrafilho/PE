import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from PIL import ImageSequence
import matplotlib.pyplot as plt
from tkinter import PhotoImage

class ImageViewer(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.current_time = tk.DoubleVar()
        self.current_time.set(0)
        
        # Placeholder image
        self.placeholder_image = Image.new("RGB", (400, 350), "lightgray")
        self.placeholder_photo = ImageTk.PhotoImage(self.placeholder_image)
        
        # Create a container for the image and parameters
        self.image_container = tk.Frame(self)
        self.image_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create a Matplotlib figure and axis for image display
        self.figure = Figure(figsize=(6, 6))
        self.axis = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.image_container)
        self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Label to display current parameters
        self.parameters_label = tk.Label(self.image_container, text="Contrast: 0\nBrightness: 0\nThreshold Min: 0\nThreshold Max: 0  ", bd=1, relief=tk.SOLID, width=20, height=4)
        self.parameters_label.pack(side=tk.TOP, anchor=tk.SW, padx=10, pady=10)
        
        # Color change button
        self.color_mode = 'grayscale'
        self.color_change_button = tk.Button(self.image_container, text="Change Color", command=self.change_color)
        self.color_change_button.pack(side=tk.TOP, anchor=tk.SW, padx=10, pady=10)
        self.is_color_changed = False
        
        # Zoom selection variables
        self.zoom_start_x = None
        self.zoom_start_y = None
        self.zoom_rect = None
        # Add a variable to track zoom mode
        self.zoom_mode_enabled = False
        
        # Bind events for zoom selection
        self.canvas.mpl_connect('button_press_event', self.on_press)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.canvas.mpl_connect('button_release_event', self.on_release)
        
        # Load magnifying glass icons using PIL
        zoom_in_image = Image.open("zoom-in.png")
        zoom_out_image = Image.open("zoom-out.png")

        # Resize the images if needed
        icon_size = (20, 20)
        zoom_in_image = zoom_in_image.resize(icon_size, Image.LANCZOS)
        zoom_out_image = zoom_out_image.resize(icon_size, Image.LANCZOS)
        
        # Create PhotoImage objects
        self.zoom_in_icon = ImageTk.PhotoImage(zoom_in_image)
        self.zoom_out_icon = ImageTk.PhotoImage(zoom_out_image)
        
        # Zoom in button
        self.zoom_in_button = tk.Button(self.image_container, image=self.zoom_in_icon, command=self.toggle_zoom_mode)
        self.zoom_in_button.image = self.zoom_in_icon  # Keep a reference
        self.zoom_in_button.pack(side=tk.TOP, anchor=tk.SW, padx=10, pady=10)

        # Zoom out button
        self.zoom_out_button = tk.Button(self.image_container, image=self.zoom_out_icon, command=self.zoom_out)
        self.zoom_out_button.image = self.zoom_out_icon  # Keep a reference
        self.zoom_out_button.pack(side=tk.TOP, anchor=tk.SW, padx=10, pady=10)
        
        
        # Segmentation button with icon
        segmentation_icon = Image.open("segmentation.png")
        segmentation_icon = segmentation_icon.resize((20, 20), Image.LANCZOS)
        segmentation_photo = ImageTk.PhotoImage(segmentation_icon)

        self.segmentation_button = tk.Button(self.image_container, command=self.toggle_segmentation_mode, image=segmentation_photo, compound="left")
        self.segmentation_button.image = segmentation_photo  # Keep a reference
        self.segmentation_button.pack(side=tk.TOP, anchor=tk.SW, padx=10, pady=10)
        
        # Chart button with icon
        chart_icon = Image.open("chart.png")
        chart_icon = chart_icon.resize((20, 20), Image.LANCZOS)
        chart_photo = ImageTk.PhotoImage(chart_icon)
        self.chart_button = tk.Button(self.image_container, command=self.generate_chart, image=chart_photo, compound="left")
        self.chart_button.image = chart_photo  # Keep a reference
        self.chart_button.pack(side=tk.TOP, anchor=tk.SW, padx=10, pady=10)

        # Segmentation variables
        self.segmentation_mode_enabled = False
        self.segment_points = []

        # Bind event for segmentation
        self.canvas.mpl_connect('button_press_event', self.on_segment_click)
        
        # Zoom factor for zooming in and out
        self.zoom_factor = 1.2

        # Set initial zoom level
        self.current_zoom_level = 1.0
        
        # Initialize image_paths attribute
        self.image_paths = []
        
        # Slider for scrolling through images/Time
        self.image_slider = ttk.Scale(self, from_=0, to=len(self.image_paths)-1, variable=self.current_time, orient=tk.HORIZONTAL, command=self.update_image_slider)
        self.image_slider.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        # Create a container for parameters and sliders
        self.parameters_container = tk.Frame(self)
        self.parameters_container.pack(side=tk.BOTTOM, pady=10)
        
        # Add entry widgets for parameters
        self.moyennage_label = tk.Label(self.parameters_container, text="Temp. averaging=")
        self.moyennage_label.pack(side=tk.LEFT, padx=5, pady=10)
        self.moyennage_entry = tk.Entry(self.parameters_container, width=10)
        self.moyennage_entry.pack(side=tk.LEFT, padx=10, pady=10)
        self.moyennage_entry.bind("<Return>", self.temporal_averaging)

        # Contrast adjustment
        self.contrast_label = tk.Label(self.parameters_container, text="Contrast=")
        self.contrast_label.pack(side=tk.LEFT, padx=5, pady=10)
        self.contrast_slider = ttk.Scale(self.parameters_container, from_=0, to=100, orient=tk.HORIZONTAL, command=self.update_contrast)
        self.contrast_slider.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Brightness adjustment
        self.brightness_label = tk.Label(self.parameters_container, text="Brightness=")
        self.brightness_label.pack(side=tk.LEFT, padx=5, pady=10)
        self.brightness_slider = ttk.Scale(self.parameters_container, from_=-100, to=100, orient=tk.HORIZONTAL, command=self.update_brightness)
        self.brightness_slider.pack(side=tk.LEFT, padx=10, pady=10)

        # Threshold adjustment
        self.threshold_min_label = tk.Label(self.parameters_container, text="Min Threshold=")
        self.threshold_min_label.pack(side=tk.LEFT, padx=5, pady=10)
        self.threshold_min_slider = ttk.Scale(self.parameters_container, from_=0, to=0.98, orient=tk.HORIZONTAL, command=self.update_threshold)
        self.threshold_min_slider.pack(side=tk.LEFT, padx=10, pady=10)

        self.threshold_max_label = tk.Label(self.parameters_container, text="Max Threshold=")
        self.threshold_max_label.pack(side=tk.LEFT, padx=5, pady=10)
        self.threshold_max_slider = ttk.Scale(self.parameters_container, from_=00.2, to=1, orient=tk.HORIZONTAL, command=self.update_threshold)
        self.threshold_max_slider.pack(side=tk.LEFT, padx=10, pady=10)
        self.threshold_max_slider.set(1)
        
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
        image_width, image_height = self.original_image.size
        
       # Placeholder image
        self.placeholder_image = Image.new("RGB", (image_width, image_height), "lightgray")
        self.placeholder_photo = ImageTk.PhotoImage(self.placeholder_image)

        # Create a container for the image and parameters with the image dimensions
        self.image_container = tk.Frame(self, width=image_width, height=image_height)
        self.image_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True) 

        # Convert the original image to a NumPy array
        self.original_image_array = np.array(self.original_image)

        # Normalize the pixel values to the range [0, 1]
        min_value = np.min(self.original_image_array)
        max_value = np.max(self.original_image_array)
        self.normalized_image_array = (self.original_image_array - min_value) / (max_value - min_value)

        # Check the shape of the normalized image array
        if len(self.normalized_image_array.shape) == 2:
            # If the array is 2D, keep it as is
            self.image = self.normalized_image_array.copy()
        elif len(self.normalized_image_array.shape) == 3:
            # If the array is 3D (RGB), convert it to grayscale
            self.image = np.mean(self.normalized_image_array, axis=-1).copy()
        
        # Reshape the 3D array to 2D for display
        displayed_image = self.image.reshape(self.image.shape[0], self.image.shape[1])

        # Check if the displayed image has the correct shape
        if displayed_image.shape[0] == 0 or displayed_image.shape[1] == 0:
            # Handle the case where the displayed image has incorrect dimensions
            print("Error: Incorrect dimensions after reshaping.")
            return
        
        self.axis.imshow(displayed_image, cmap='gray')  # Display the reshaped 2D image
        self.canvas.draw_idle()

        self.update_displayed_image()
        
        # Initialize images_for_temporal_averaging list with the first image
        self.images_for_temporal_averaging = [self.normalized_image_array]

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
            self.color_change_button.pack(side=tk.TOP, anchor=tk.SW, padx=10, pady=10)  # Pack the button again
            
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

        if threshold_min >= threshold_max:
            # Adjust the values to ensure threshold_min is always less than threshold_max
            threshold_max = max(threshold_max, threshold_min + 0.01)  # Adjust threshold_max to be slightly higher than threshold_min
            self.threshold_max_slider.set(threshold_max)  # Update the slider value
        if threshold_max <= threshold_min:
            # Adjust the values to ensure threshold_max is always greater than threshold_min
            threshold_min = min(threshold_min, threshold_max - 0.01)  # Adjust threshold_min to be slightly lower than threshold_max
            self.threshold_min_slider.set(threshold_min)  # Update the slider value
            
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
        #if self.color_mode == 'inverted':
         #   displayed_image = 1 - self.image
        #else:
         #   displayed_image = self.image

        #self.axis.imshow(displayed_image, cmap='gray')
        #self.canvas.draw_idle()
        # Get the original image shape
        original_shape = self.original_image_array.shape

        # Reshape the image to its original shape
        displayed_image = self.image.reshape(original_shape)

        # Apply color mode
        displayed_image = self.apply_color_mode(displayed_image)
        
        # Resize the image based on the current zoom level
        resized_image = Image.fromarray((displayed_image * 255).astype(np.uint8))
        new_size = tuple(int(dim * self.current_zoom_level) for dim in original_shape[:2])
        resized_image = resized_image.resize(new_size, Image.LANCZOS)
        
        # Update the displayed image using Matplotlib
        # displayed_image = self.apply_color_mode(self.image)
        # Update the displayed image using Matplotlib
        self.axis.imshow(resized_image, cmap='gray')
        self.canvas.draw_idle()
        
    def apply_color_mode(self, image):
        # Apply the selected color mode to the image
        if self.color_mode == 'inverted' and self.is_color_changed:
            return 1.0 - image.reshape(self.original_image_array.shape)  # Reshape to the original shape
        else:
            return image

    def change_color(self):
        #self.color_mode = 'inverted' if self.color_mode == 'grayscale' else 'grayscale'
        #self.update_displayed_image()
        #self.color_change_button.pack(side=tk.TOP, anchor=tk.NE, padx=10, pady=10)  # Pack the button again    
        self.is_color_changed = not self.is_color_changed
        self.color_mode = 'inverted' if self.is_color_changed else 'grayscale'
        self.update_displayed_image()
        self.color_change_button.config(text="Change Color" if not self.is_color_changed else "Revert Color")
        
    def zoom_in(self):
        # Zoom in the image
        self.current_zoom_level *= self.zoom_factor
        self.update_displayed_image()

    def zoom_out(self):
        # Zoom out the image
        self.current_zoom_level /= self.zoom_factor
        self.update_displayed_image()
    
    def toggle_zoom_mode(self):
        # Toggle the zoom mode on/off
        self.zoom_mode_enabled = not self.zoom_mode_enabled
            
    # Zoom Selection
    def on_press(self, event):
        # Check if zoom mode is enabled
        if not self.zoom_mode_enabled:
            return

        # Store the starting position for zoom selection
        self.zoom_start_x = event.xdata
        self.zoom_start_y = event.ydata

    def on_motion(self, event):
        
        # Check if zoom mode is enabled
        if not self.zoom_mode_enabled:
            return

        # Update the zoom rectangle during motion
        if self.zoom_start_x is not None and self.zoom_start_y is not None:
            current_x = event.xdata
            current_y = event.ydata

            if self.zoom_rect:
                self.axis.patches.remove(self.zoom_rect)

            width = current_x - self.zoom_start_x
            height = current_y - self.zoom_start_y

            self.zoom_rect = plt.Rectangle((self.zoom_start_x, self.zoom_start_y), width, height,
                                       linewidth=1, edgecolor='r', facecolor='none')
            self.axis.add_patch(self.zoom_rect)
            self.canvas.draw()

    def on_release(self, event):
        # Check if zoom mode is enabled
        if not self.zoom_mode_enabled:
            return
        
        # Perform zoom based on the selected area
        if self.zoom_start_x is not None and self.zoom_start_y is not None:
            current_x = event.xdata
            current_y = event.ydata

            width = current_x - self.zoom_start_x
            height = current_y - self.zoom_start_y

            if width != 0 and height != 0:
                # Calculate the zoomed area and update the displayed image
                zoomed_area = self.image[int(self.zoom_start_y):int(current_y), int(self.zoom_start_x):int(current_x)]


                # Update the displayed image using Matplotlib
                self.axis.imshow(zoomed_area, cmap='gray')
                self.canvas.draw_idle()

            # Reset zoom selection variables
            self.zoom_start_x = None
            self.zoom_start_y = None
            self.zoom_rect = None
            
            
    # SEGMENTATION
    def toggle_segmentation_mode(self):
        # Toggle the segmentation mode on/off
        self.segmentation_mode_enabled = not self.segmentation_mode_enabled

        if self.segmentation_mode_enabled:
            # Clear previous segment points
            self.segment_points = []
            self.segmentation_button.config(text="Stop")
        else:
            # Process segments and update the displayed image
            self.process_segments()
            self.segmentation_button.config(text="Start")

    def on_segment_click(self, event):
        # Check if segmentation mode is enabled
        if not self.segmentation_mode_enabled:
            return

        # Add the clicked point to the segment points
        self.segment_points.append((event.xdata, event.ydata))

        # Draw a red dot at the clicked point
        self.axis.plot(event.xdata, event.ydata, 'ro')
        self.canvas.draw()

    def process_segments(self):
        if len(self.segment_points) < 3:
            return  # At least 3 points needed to form a segment

        # Add the first point to the end to create a closed segment
        self.segment_points.append(self.segment_points[0])

        # Convert segment points to NumPy array
        segment_points_array = np.array(self.segment_points)

        # Draw the closed segment on the displayed image
        self.axis.plot(segment_points_array[:, 0], segment_points_array[:, 1], 'r-')
        self.canvas.draw()
        
    def generate_chart(self):
        # Generate a chart based on the points from the segmentation
        if len(self.segment_points) < 3:
            return  # At least 3 points needed to form a chart

        # Extract x and y coordinates from segment points
        x_coordinates, y_coordinates = zip(*self.segment_points)

        # Create a scatter plot using Matplotlib
        plt.scatter(x_coordinates, y_coordinates, color='blue')
        plt.title("Chart Generated from Segmentation Points")
        plt.xlabel("X-coordinate")
        plt.ylabel("Y-coordinate")
        plt.gca().invert_yaxis()
        plt.show()