import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
import os
from matplotlib.figure import Figure
from matplotlib.widgets import Slider
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from PIL import ImageSequence
import matplotlib.pyplot as plt
from tkinter import PhotoImage
import tifffile 
import imageio
import csv
from tkinter import messagebox
import matplotlib.text as text
from pprint import pprint


class ImageViewer(ttk.Frame):
    def __init__(self, master,GUI=None):
        super().__init__(master)
        self.canaux = {0:np.zeros((1,1,1)), 1:np.zeros((1,1,1))}
        self.current_index = 0 #Index for Slider
        self.normalized_image_array_red = np.zeros((1,1,1))
        self.normalized_image_array_green = np.zeros((1,1,1))
       
        self.GUI=GUI        
        self.is_image_black = True
        self.saturation_pixels_min = 0.1
        self.saturation_pixels_max = 99.8
        self.contrast_value = 0
        self.brightness_value = 0        
        # self.sequence = imageio.volread(r'C:\Users\carlo\Downloads\transfer_6891262_files_d43c2e32\220728-S2_04_500mV.ome.tiff')

        self.data_viewer = None
        self.graph_viewer=None

        self.current_time = tk.DoubleVar()
        self.current_time.set(0)
        
        # Add a variable to track whether panning mode is enabled
        self.panning_mode_enabled = False
        self.panning_start_x = None
        self.panning_start_y = None
        
        # Add a variable to track whether the user is currently zooming
        self.zooming = False

        #Image array
        self.normalized_image_array = np.array([])
        self.selected_index = 0

        # Placeholder image
        self.placeholder_image = Image.new("RGB", (400, 350), "lightgray")
        self.placeholder_photo = ImageTk.PhotoImage(self.placeholder_image)
        
        # Create a container for the image and parameters
        self.image_container = ttk.Frame(self)
        self.image_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create a Matplotlib figure and axis for image display
        #self.figure = Figure(figsize=(5, 5))
        self.figure = plt.Figure(figsize=(5, 5))
        self.axis = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.image_container)
        self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        ###
        self.canvas.draw()
        ###
        
        # Label to display current parameters
        self.parameters_label = tk.Label(self.image_container, text="Contrast: 0\nBrightness: 0\nThreshold Min: 0\nThreshold Max: 0  ", bd=1, relief=tk.SOLID, width=20, height=4)
        self.parameters_label.pack(side=tk.TOP, anchor=tk.SW, padx=10, pady=10)

        self.selected_channel = 1
        # Red channel button
        self.color_mode = 'gray'
        self.red_button = tk.Button(self.image_container, text="Red Channel", command=self.select_red_channel)
        self.red_button.pack(side=tk.TOP, anchor=tk.SW, padx=10, pady=10)
        self.red_button.config(relief=SUNKEN)
        self.is_red_button = True

        # Green channel button
        self.color_mode = 'gray'
        self.green_button= tk.Button(self.image_container, text="Green Channel", command=self.select_green_channel)
        self.green_button.pack(side=tk.TOP, anchor=tk.SW, padx=10, pady=10)
        self.is_green_button = False
        # Color change button
        self.color_mode = 'gray'
        self.is_color_changed = False
        self.color_change_button = tk.Button(self.image_container, text="Change Color", command=self.change_color)
        self.color_change_button.pack(side=tk.TOP, anchor=tk.SW, padx=10, pady=10)
        
        
        # Bind events for zoom using mouse wheel
        self.canvas.mpl_connect('scroll_event', self.on_scroll)
        
        # Bind events for panning
        self.canvas.mpl_connect('button_press_event', self.on_pan_press)
        self.canvas.mpl_connect('motion_notify_event', self.on_pan_motion)
        self.canvas.mpl_connect('button_release_event', self.on_pan_release)
        
        # Bind events for zoom start and end
        self.canvas.mpl_connect('button_press_event', self.on_zoom_start)
        self.canvas.mpl_connect('button_release_event', self.on_zoom_end)
        
        # Zoom selection variables
        self.zoom_start_x = None
        self.zoom_start_y = None
        self.zoom_rect = None
        # Add a variable to track zoom mode
        self.zoom_mode_enabled = False
        
        self.zoom_mode = False  # Initialize zoom_mode attribute
        
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
        self.zoom_in_button = ttk.Button(self.image_container, image=self.zoom_in_icon, command=self.zoom_in)
        self.zoom_in_button.image = self.zoom_in_icon  # Keep a reference
        self.zoom_in_button.pack(side=tk.TOP, anchor=tk.SW, padx=10, pady=10)

        # Zoom out button
        self.zoom_out_button = ttk.Button(self.image_container, image=self.zoom_out_icon, command=self.zoom_out)
        self.zoom_out_button.image = self.zoom_out_icon  # Keep a reference
        self.zoom_out_button.pack(side=tk.TOP, anchor=tk.SW, padx=10, pady=10)
        
        # Segmentation button with icon
        segmentation_icon = Image.open("segmentation.png")
        segmentation_icon = segmentation_icon.resize((20, 20), Image.LANCZOS)
        segmentation_photo = ImageTk.PhotoImage(segmentation_icon)

        self.segmentation_button = ttk.Button(self.image_container, command=self.toggle_segmentation_mode, image=segmentation_photo, compound="left")
        self.segmentation_button.image = segmentation_photo  # Keep a reference
        self.segmentation_button.pack(side=tk.TOP, anchor=tk.SW, padx=10, pady=10)
        
        # Chart button with icon
        chart_icon = Image.open("chart.png")
        chart_icon = chart_icon.resize((20, 20), Image.LANCZOS)
        chart_photo = ImageTk.PhotoImage(chart_icon)
        #self.chart_button = ttk.Button(self.image_container, command=self.generate_chart, image=chart_photo, compound="left")
        #self.chart_button.image = chart_photo  # Keep a reference
        #self.chart_button.pack(side=tk.TOP, anchor=tk.SW, padx=10, pady=10)

        # Segmentation variables
        self.segmentation_mode_enabled = False
        self.segment_x_points = []
        self.segment_y_points = []
        self.x_in = []
        self.y_in = []
        self.listes_graphs=[]
        self.temp_ROI_points = [[] for _ in range(250)]
        self.ROI_index = 0
        self.ROI_objects = {}
        self.id_color=-1 
        self.marker_styles_point = ['b.', 'g.', 'r.', 'c.', 'm.', 'y.', 'k.', 'w.']
        self.marker_styles_line = ['b-', 'g-', 'r-', 'c-', 'm-', 'y-', 'k-', 'w-']

        #Command Show_tags
        self.show_tags_var = tk.BooleanVar()
        self.show_tags_var.set(False)  # Par défaut, ne pas afficher les tags

        self.show_tags_checkbutton = tk.Checkbutton(self.image_container, text="Show Tags", variable=self.show_tags_var, command=self.update_displayed_image)
        self.show_tags_checkbutton.pack()

        self.tag_artists = []


        # Bind event for segmentation
        self.canvas.mpl_connect('button_press_event', self.on_segment_click)
        
        # Zoom factor for zooming in and out
        self.zoom_factor = 1.1

        # Set initial zoom level
        self.current_zoom_level = 1.0
        self.previous_x = None
        self.previous_y = None
        
        # Slider for scrolling through images/Time
        #self.image_slider = ttk.Scale(self, from_=0, to=len(self.normalized_image_array)-1, variable=self.current_time, orient=tk.HORIZONTAL, command=self.update_image_slider)
        #self.image_slider.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        # Create a container for parameters and sliders
        self.parameters_container = ttk.Frame(self)
        self.parameters_container.pack(side=tk.TOP, pady=1)

        # Brightness adjustment
        self.brightness_label = ttk.Label(self.parameters_container, text="Brightness=")
        self.brightness_label.grid(row=0, column=0, padx=5, pady=5)
        self.brightness_slider = ttk.Scale(self.parameters_container, from_=-100, to=100, orient=tk.HORIZONTAL, command=self.update_brightness)
        self.brightness_slider.grid(row=0, column=1, padx=10, pady=5)

        # Contrast adjustment
        self.contrast_label = ttk.Label(self.parameters_container, text="Contrast=")
        self.contrast_label.grid(row=0, column=2, padx=5, pady=5)
        self.contrast_slider = ttk.Scale(self.parameters_container, from_=0, to=100, orient=tk.HORIZONTAL, command=self.update_contrast)
        self.contrast_slider.grid(row=0, column=3, padx=10, pady=5)

        # Temporal averaging entry
        self.moyennage_label = ttk.Label(self.parameters_container, text="Temporal averaging=")
        self.moyennage_label.grid(row=0, column=4, padx=5, pady=5)
        self.moyennage_entry = ttk.Entry(self.parameters_container, width=10)
        self.moyennage_entry.grid(row=0, column=5, padx=10, pady=5)
        self.moyennage_entry.bind("<Return>", self.update_window_size)

        # Threshold adjustment
        self.threshold_min_label = ttk.Label(self.parameters_container, text="Min Threshold=")
        self.threshold_min_label.grid(row=1, column=0, padx=5, pady=5)
        self.threshold_min_slider = ttk.Scale(self.parameters_container, from_=0, to=254, orient=tk.HORIZONTAL, command=self.update_threshold)
        self.threshold_min_slider.grid(row=1, column=1,padx=10,pady=5)

        self.threshold_max_label = ttk.Label(self.parameters_container,text="Max Threshold=")
        self.threshold_max_label.grid(row=1,column=2,padx=5,pady=5)
        self.threshold_max_slider = ttk.Scale(self.parameters_container ,from_=1,to =255 ,orient=tk.HORIZONTAL ,command=self.update_threshold )
        self.threshold_max_slider.grid(row = 1,column = 3,padx = 10,pady = 5 )
        self.threshold_max_slider.set(255)

        # Save button
        self.save_button = tk.Button(self.parameters_container,text="Apply to all images ",command=self.save_parameters )
        self.save_button.grid(row = 1,column = 4,pady = 5 )
        # Temporal averaging variables
        self.window_size = 1  # Initial window size
        self.images_for_temporal_averaging = []  # List to store images for averaging
                
        # Keep a reference to the original image for reset functionality
        self.original_image = None
        self.image = None
        self.color_mode = 'gray'  # Initial color mode
        
        #self.sequence=imageio.volread(r'C:\Users\carlo\Downloads\transfer_6891262_files_d43c2e32\220728-S2_04_500mV.ome.tiff')
        self.reset_image()
        self.canaux = {}


    
    def disable_functionalities_pre_load(self):
        self.red_button.config(state="disabled")
        self.green_button.config(state="disabled")
        self.color_change_button.config(state="disabled")
        self.zoom_in_button.config(state="disabled")
        self.zoom_out_button.config(state="disabled")
        self.segmentation_button.config(state="disabled")
        self.contrast_slider.config(state="disabled")
        self.brightness_slider.config(state="disabled")
        self.threshold_min_slider.config(state="disabled")
        self.threshold_max_slider.config(state="disabled")
        #self.image_slider.config(state="disabled")
        self.moyennage_entry.config(state="disabled")
        self.save_button.config(state="disabled")
        self.show_tags_checkbutton.config(state="disabled")
    
    def enable_functionalities_post_load(self):
        self.red_button.config(state="normal")
        self.green_button.config(state="normal")
        self.color_change_button.config(state="normal")
        self.zoom_in_button.config(state="normal")
        self.zoom_out_button.config(state="normal")
        self.segmentation_button.config(state="normal")
        self.contrast_slider.config(state="normal")
        self.brightness_slider.config(state="normal")
        self.threshold_min_slider.config(state="normal")
        self.threshold_max_slider.config(state="normal")
        #self.image_slider.config(state="normal")
        self.moyennage_entry.config(state="normal")
        self.save_button.config(state="normal")
        self.show_tags_checkbutton.config(state="normal")


    def set_data_viewer(self, data_viewer):
        self.data_viewer = data_viewer

    def set_graph_viewer(self, graph_viewer):
        self.graph_viewer = graph_viewer
    def save_parameters(self):
        
        self.save_button.config(relief=SUNKEN)
        if self.selected_channel == 0:
            self.canaux[0] = np.clip(self.normalized_image_array_green * (1.0 + self.contrast_value)+ self.brightness_value, 0, 255).astype(np.uint8)
            self.canaux[0][self.normalized_image_array_green<self.threshold_min] = 0
            self.canaux[0][self.normalized_image_array_green>self.threshold_max] = 255
        elif self.selected_channel == 1:
            self.canaux[1] = np.clip(self.normalized_image_array_red * (1.0 + self.contrast_value)+ self.brightness_value, 0, 255).astype(np.uint8)
            self.canaux[1][self.normalized_image_array_red<self.threshold_min] = 0
            self.canaux[1][self.normalized_image_array_red>self.threshold_max] = 255
        self.save_button.config(relief=RAISED)

    def clean_display_seg(self):
        self.axis.clear()
        self.ROI_objects = {}
        self.ROI_index = 0
        self.update_ROI_visibility_list()
        self.show_tags_var.set(False)

    def load_image(self, image_path):

        # Load and display image using Matplotlib
        #self.original_image = Image.open(image_path)
        self.original_image = tifffile.imread(image_path)
        #print("Original Image:", self.original_image.shape)
        image_width, image_height = self.original_image[0,0].shape
        #image_width, image_height = self.original_image.size
        
        red_images = np.copy(self.original_image[1])
        green_images = np.copy(self.original_image[0])
        
        

        
       # Placeholder image
        self.placeholder_image = Image.new("RGB", (image_width, image_height), "lightgray")
        self.placeholder_photo = ImageTk.PhotoImage(self.placeholder_image)
   
        self.image_container = tk.Frame(self, width=image_width, height=image_height)
        self.image_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True) 
        
        min_value_red = np.percentile(red_images[0],0.1)
        max_value_red = np.percentile(red_images[0],99.8)
        self.normalized_image_array_red = (255*np.clip(red_images,min_value_red,max_value_red)/(max_value_red- min_value_red)).astype(np.uint8)
        
        del red_images
        min_value_green = np.percentile(green_images[0],0.1)
        max_value_green = np.percentile(green_images[0],99.8)
        self.normalized_image_array_green = (255*np.clip(green_images,min_value_green,max_value_green)/(max_value_green- min_value_green)).astype(np.uint8)
        
        if np.mean(green_images[0])>2**15: #Si le fond de l'image est blanc, le convertir en noir
            self.normalized_image_array_green = 255- self.normalized_image_array_green
            self.normalized_image_array_red = 255- self.normalized_image_array_red
            self.is_image_black = False
        del green_images
        self.canaux = {0: np.copy(self.normalized_image_array_green),
                        1: np.copy(self.normalized_image_array_red)}
        
        self.image_display = self.axis.imshow(self.canaux[self.selected_channel][self.current_index], cmap=self.color_mode)
    
        
        self.image_display = self.axis.imshow(self.normalized_image_array_red[self.current_index], cmap='gray')
        ax_slider = self.figure.add_axes([0.2, 0.05, 0.65, 0.03])
        self.slider = Slider(ax_slider, 'Image', 0, self.canaux[1].shape[0]-1, valinit=0)
        print(self.canaux[1].shape[0])
        self.slider.on_changed(self.update_image)

    def update_image(self,value = None):
        self.current_index = int(self.slider.val)
        self.image_display.set_data(self.canaux[self.selected_channel][self.current_index])
        
        
        self.update_displayed_image()
        

    def update_time_slider(self, max_time):
        self.time_slider.configure(to=max_time)
        
    def get_parameters(self):
        # Get parameter values
        moyennage = int(self.moyennage_entry.get())
        contrast = self.contrast_slider.get()
        return moyennage, contrast
    
    def update_contrast(self, *args):
        # Get contrast value from the slider
        self.contrast_value = round(self.contrast_slider.get() / 100.0, 2)  # Round to two decimal places

        # Apply contrast adjustment
 
        self.contrast_brightness_threshold()
        self.update_displayed_image()
        self.update_parameters_label()

        # Update the displayed image using Matplotlib------------------------
        # self.axis.imshow(contrasted_image, cmap='gray')
        # self.canvas.draw_idle()

    def contrast_brightness_threshold(self):
        # Calculate the contrasted image by multiplying by the contrast value
        if self.selected_channel == 0:
            self.canaux[0][self.current_index] = np.clip(self.normalized_image_array_green[self.current_index] * (1.0 + self.contrast_value)+ self.brightness_value, 0, 255).astype(np.uint8)  # Normalize to [0, 1]
            self.canaux[0][self.current_index][self.normalized_image_array_green[self.current_index]<self.threshold_min] = 0
            self.canaux[0][self.current_index][self.normalized_image_array_green[self.current_index]>self.threshold_max] = 255
        elif self.selected_channel == 1:
            self.canaux[1][self.current_index] = np.clip(self.normalized_image_array_red[self.current_index] * (1.0 + self.contrast_value)+ self.brightness_value, 0, 255).astype(np.uint8)  # Normalize to [0, 1]
            self.canaux[1][self.current_index][self.normalized_image_array_red[self.current_index]<self.threshold_min] = 0
            self.canaux[1][self.current_index][self.normalized_image_array_red[self.current_index]>self.threshold_max] = 255
        
            
            
        #return thresholded_image[1]
 
    
    def update_brightness(self, *args):
        # Get brightness value from the slider
        self.brightness_value = round(self.brightness_slider.get(), 2)  # Round to two decimal places
        
        self.contrast_brightness_threshold()
        self.update_displayed_image()
        
        self.update_parameters_label()

    def load_image_at_index(self, time):
        if not self.normalized_image_array_red.any():
            return  # No images loaded yet

        if time < 0 or time >= len(self.normalized_image_array_red):
            return  # Handle the case when the specified time is out of bounds

        selected_image_path = self.normalized_image_array_red[time]
        self.update_displayed_image()
        
    def update_image_slider(self):
        self.selected_index = int(self.image_slider.get())
        print("Selected Index:", self.selected_index)
        self.update_displayed_image(self.selected_index)
    
    def reset_image(self):
        # Reset the image to its original state
        if self.original_image:
            self.image = self.normalized_image_array_red.copy()
            self.image_slider.set(0)
            self.contrast_slider.set(0)  # Update the contrast slider
            self.brightness_slider.set(0)  # Update the brightness slider
            self.threshold_min_slider.set(0)  # Update the min threshold slider
            self.threshold_max_slider.set(1)  # Update the max threshold slider
            self.axis.clear()
            self.axis.imshow(self.image, cmap='gray')
            self.canvas.draw_idle()
            self.color_change_button.pack(side=tk.TOP, anchor=tk.SW, padx=10, pady=10)  # Pack the button again
            
    def update_window_size(self, val = None):
        # Get the window size for temporal averaging from the entry widget
        window_size = int(self.moyennage_entry.get())

        # Check if the window size is valid
        #if window_size < 1 or window_size > len(self.image_paths):
        #    return

        # Update the window size and reload images for temporal averaging
        self.window_size = window_size
        self.temporal_averaging()
        self.update_displayed_image()

            

    def temporal_averaging(self):
        # Check if there are images for temporal averaging
        nb_images = self.canaux[1].shape[0]
        for i in range(nb_images-self.window_size+1):
            self.normalized_image_array_green[i] = np.mean(self.normalized_image_array_green[i:i+self.window_size,:,:], axis = 0)
            self.normalized_image_array_red[i] = np.mean(self.normalized_image_array_red[i:i+self.window_size,:,:], axis = 0)
        self.canaux = {0: np.copy(self.normalized_image_array_green),
                        1: np.copy(self.normalized_image_array_red)}
       
            
    def update_threshold(self, *args):
        # Get threshold values from the sliders
        self.threshold_min = round(self.threshold_min_slider.get())  
        self.threshold_max = round(self.threshold_max_slider.get())  
        
        # Update the threshold labels with the current values
        #self.threshold_min_value_label.config(text=f"Threshold Min: {threshold_min}")
        #self.threshold_max_value_label.config(text=f"Threshold Max: {threshold_max}")

        if self.threshold_min >= self.threshold_max:
            # Adjust the values to ensure threshold_min is always less than threshold_max
            self.threshold_max = max(self.threshold_max, self.threshold_min + 1)  # Adjust threshold_max to be slightly higher than threshold_min
            self.threshold_max_slider.set(self.threshold_max)  # Update the slider value
        if self.threshold_max <= self.threshold_min:
            # Adjust the values to ensure threshold_max is always greater than threshold_min
            self.threshold_min = min(self.threshold_min, self.threshold_max - 1)  # Adjust threshold_min to be slightly lower than threshold_max
            self.threshold_min_slider.set(self.threshold_min)  # Update the slider value
        # self.threshold()
        self.contrast_brightness_threshold()
        self.update_displayed_image()  
        # Update the parameters label with the current values
        self.update_parameters_label()
        

    def update_parameters_label(self):
        # Get the current label text
        
        parameters_text = f"Contrast: {self.contrast_value}\nBrightness: {self.brightness_value}\nThreshold Min: {self.threshold_min}\nThreshold Max: {self.threshold_max}  "
        self.parameters_label.config(text=parameters_text)
    
    def update_displayed_image(self):
        #Update the displayed image using Matplotlib
        
        
        if self.is_green_button:
            self.axis.imshow(self.canaux[0][self.current_index], cmap=self.color_mode)
        if self.is_red_button:
            self.axis.imshow(self.canaux[1][self.current_index], cmap=self.color_mode)

        if(self.is_green_button and self.is_red_button):
            self.axis.imshow(np.dstack((self.canaux[1][self.current_index], self.canaux[0][self.current_index], np.zeros_like(self.canaux[0][self.current_index]))))
      

        dic=self.get_dic_ROI()
        if not self.show_tags_var.get():
            self.remove_all_tags()  # Masquer tous les tags si la case à cocher n'est pas cochée
        if self.show_tags_var.get():
            for index in dic.keys():  # Parcours de tous les indices dans le dictionnaire
                if not self.tag_artists or index-1 >= len(self.tag_artists):
                    coords=dic.get(index, {}).get('coord') 
                    liste_x=[x for x, y in coords]
                    liste_y=[y for x, y in coords]
                    self.create_tag(index, min(liste_x), min(liste_y))
                self.display_tag(index)


        # Rafraîchir l'affichage pour voir les modifications
        self.canvas.draw_idle()
        """ ---------------------------------------------------------------------------
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
        """
    def apply_color_mode(self, image):
        # Apply the selected color mode to the image
        if self.color_mode == 'gray_r' and self.is_color_changed:
            return 1.0 - image.reshape(self.original_image[0,0].shape)  # Reshape to the original shape
        else:
            return image
        
    def select_green_channel(self):
        self.selected_channel = 0
        if self.green_button.config('relief')[-1] == 'sunken':
            self.green_button.config(relief=RAISED)
        else:
            self.green_button.config(relief=SUNKEN)
        self.is_green_button = not self.is_green_button
        self.update_image()

    def select_red_channel(self):
        self.selected_channel = 1
        if self.red_button.config('relief')[-1] == 'sunken':
            self.red_button.config(relief=RAISED)
        else:
            self.red_button.config(relief=SUNKEN)
        self.is_red_button = not self.is_red_button
        self.update_image()

    def change_color(self):
        #self.color_mode = 'inverted' if self.color_mode == 'grayscale' else 'grayscale'
        #self.update_displayed_image()
        #self.color_change_button.pack(side=tk.TOP, anchor=tk.NE, padx=10, pady=10)  # Pack the button again    
        self.is_color_changed = not self.is_color_changed
        self.color_mode = 'gray_r' if self.is_color_changed else 'gray'
        self.update_displayed_image()
        self.color_change_button.config(text="Change Color" if not self.is_color_changed else "Revert Color")

## START ZOOM        
    def zoom_in(self):
        ''' OLD METHOD
        # Zoom in the image
        self.current_zoom_level *= self.zoom_factor
        self.update_displayed_image()
        '''
        xlim = self.axis.get_xlim()  # Get current x-axis limits
        ylim = self.axis.get_ylim()  # Get current y-axis limits
        zoom_factor = 1.1  # Zoom factor
        new_xlim = (xlim[0] / zoom_factor, xlim[1] / zoom_factor)  # New x-axis limits
        new_ylim = (ylim[0] / zoom_factor, ylim[1] / zoom_factor)  # New y-axis limits
        self.axis.set_xlim(new_xlim)  # Set new x-axis limits
        self.axis.set_ylim(new_ylim)  # Set new y-axis limits
        self.canvas.draw_idle()  # Redraw canvas
        

    def zoom_out(self):
        '''OLD METHOD
        # Zoom out the image
        self.current_zoom_level /= self.zoom_factor
        self.update_displayed_image()
        '''
        xlim = self.axis.get_xlim()  # Get current x-axis limits
        ylim = self.axis.get_ylim()  # Get current y-axis limits
        zoom_factor = 1.1  # Zoom factor
        new_xlim = (xlim[0] * zoom_factor, xlim[1] * zoom_factor)  # New x-axis limits
        new_ylim = (ylim[0] * zoom_factor, ylim[1] * zoom_factor)  # New y-axis limits
        self.axis.set_xlim(new_xlim)  # Set new x-axis limits
        self.axis.set_ylim(new_ylim)  # Set new y-axis limits
        self.canvas.draw_idle()  # Redraw canvas
        
    def reset_zoom(self):
        self.current_zoom_level = 1.0
        self.axis.set_xlim(0, 1)
        self.axis.set_ylim(0, 1)
        self.canvas.draw_idle()
        
    def toggle_zoom_mode(self):
        # Toggle the zoom mode on/off
        #self.zoom_mode_enabled = not self.zoom_mode_enabled
        self.zoom_mode = not self.zoom_mode
        # Reset panning mode when zoom mode is toggled
        self.panning_mode_enabled = False
            
    # Zoom Selection
    def on_press(self, event):
        ##### OLD METHOD
        
        # Check if zoom mode is enabled
        #if not self.zoom_mode_enabled:
        #    return

        # Store the starting position for zoom selection
        #self.zoom_start_x = event.xdata
        #self.zoom_start_y = event.ydata
        
        #####
        self.previous_x = event.x
        self.previous_y = event.y
        

    def on_motion(self, event):
        
        ''' OLD METHOD
        
        # Check if zoom mode is enabled
        if not self.zoom_mode_enabled:
            return

        # Update the zoom rectangle during motion
        if self.zoom_start_x is not None and self.zoom_start_y is not None:
            current_x = event.xdata
            current_y = event.ydata

            if self.zoom_rect:
                #self.axis.patches.remove(self.zoom_rect)
                self.zoom_rect.set_width(current_x - self.zoom_start_x)
                self.zoom_rect.set_height(current_y - self.zoom_start_y)
                self.zoom_rect.set_xy((self.zoom_start_x, self.zoom_start_y))

            else:            

                width = current_x - self.zoom_start_x
                height = current_y - self.zoom_start_y

                self.zoom_rect = plt.Rectangle((self.zoom_start_x, self.zoom_start_y), width, height,
                                       linewidth=1, edgecolor='r', facecolor='none')
                self.axis.add_patch(self.zoom_rect)
            
            #self.canvas.draw()
            self.canvas.draw_idle()

        '''
        '''
        if event.button == "None":
            return

        if self.previous_x is None or self.previous_y is None:
            return

        if event.button == 1:
            dx = event.x - self.previous_x
            dy = event.y - self.previous_y

            self.axis.set_xlim(self.axis.get_xlim() - dx * 0.01)
            self.axis.set_ylim(self.axis.get_ylim() - dy * 0.01)
            self.canvas.draw_idle()

        self.previous_x = event.x
        self.previous_y = event.y
        '''
        # Check if zoom mode is enabled and if the user is zooming
        if self.zoom_mode and self.zooming:
            # Calculate the difference in x and y coordinates
            dx = event.x - self.previous_x
            dy = event.y - self.previous_y
        
            # Update the x-axis and y-axis limits accordingly
            xlim = self.axis.get_xlim()
            ylim = self.axis.get_ylim()
            self.axis.set_xlim(xlim[0] - dx * 0.01, xlim[1] - dx * 0.01)
            self.axis.set_ylim(ylim[0] - dy * 0.01, ylim[1] - dy * 0.01)
        
            # Redraw the canvas
            self.canvas.draw_idle()
    
        # Update the previous x and y coordinates
        self.previous_x = event.x
        self.previous_y = event.y
        
    
    
    def on_release(self, event):
        ''' OLD METHOD
        
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
        '''
        self.previous_x = None
        self.previous_y = None
        
            
            
    def on_scroll(self, event):
        # Check if zoom mode is enabled
        if not self.zoom_mode:
            return
        # Get the current zoom level
        zoom_factor = 1.1 if event.button == 'up' else 1 / 1.1
        self.current_zoom_level *= zoom_factor
        '''
        xlim = self.axis.get_xlim()
        ylim = self.axis.get_ylim()
        self.axis.set_xlim(xlim[0] * zoom_factor, xlim[1] * zoom_factor)
        self.axis.set_ylim(ylim[0] * zoom_factor, ylim[1] * zoom_factor)
        '''
        xlim = self.axis.get_xlim()
        ylim = self.axis.get_ylim()
        center_x = (xlim[0] + xlim[1]) / 2
        center_y = (ylim[0] + ylim[1]) / 2
        new_width = (xlim[1] - xlim[0]) * zoom_factor
        new_height = (ylim[1] - ylim[0]) * zoom_factor
        self.axis.set_xlim(center_x - new_width / 2, center_x + new_width / 2)
        self.axis.set_ylim(center_y - new_height / 2, center_y + new_height / 2)
       
        
        self.canvas.draw_idle()
        #self.update_displayed_image()

    def on_pan_press(self, event):
        # Check if panning mode is enabled
        if not self.panning_mode_enabled:
            return
        self.panning_start_x = event.xdata
        self.panning_start_y = event.ydata

    def on_pan_motion(self, event):
        # Check if panning mode is enabled and a starting point is set
        if not self.panning_mode_enabled or self.panning_start_x is None or self.panning_start_y is None:
            return
        current_x = event.xdata
        current_y = event.ydata
        if current_x is not None and current_y is not None:
            delta_x = current_x - self.panning_start_x
            delta_y = current_y - self.panning_start_y
            self.axis.set_xlim(self.axis.get_xlim() - delta_x)
            self.axis.set_ylim(self.axis.get_ylim() - delta_y)
            self.canvas.draw_idle()

    def on_pan_release(self, event):
        # Reset panning variables
        self.panning_start_x = None
        self.panning_start_y = None
        
    def on_zoom_start(self, event):
        # Check if zoom mode is enabled
        if self.zoom_mode_enabled:
            # Set zooming flag to True
            self.zooming = True
            # Change cursor to a hand
            self.canvas.config(cursor='hand')

    def on_zoom_end(self, event):
        # Check if zoom mode was active
        if self.zooming:
            # Reset zooming flag
            self.zooming = False
            # Restore cursor to default
            self.canvas.config(cursor='')    
## END ZOOM        
        
        
    # SEGMENTATION
    def toggle_segmentation_mode(self):
        # Toggle the segmentation mode on/off
        self.segmentation_mode_enabled = not self.segmentation_mode_enabled

        if self.segmentation_mode_enabled:
            # Clear previous segment points
            self.update_color()
            self.segment_x_points = []
            self.segment_y_points = []
            self.temp_ROI_points = []
            self.segmentation_button.config(text="Stop Segmentation")
        else:
            # Process segments and update the displayed image
            self.process_segments()
            self.segmentation_button.config(text="Start Segmentation")
 
 
    def on_segment_click(self, event):

        # Check if segmentation mode is enabled
        if not self.segmentation_mode_enabled:
            return

        # Add the clicked point to the segment points
        self.segment_x_points.append(event.xdata)
        self.segment_y_points.append(event.ydata)

        # Draw a red dot at the clicked point
        self.temp_ROI_points.append(self.axis.plot(event.xdata, event.ydata, self.marker_styles_point[self.id_color]))
        self.canvas.draw()

    def reset_context_for_segments_csv(self):
        #self.id_color = -1
        return
        #self.clear_segments()

    def draw_segments_from_csv(self, coordinates):
        self.temp_ROI_points = []
        
        if (len(coordinates) < 3):
            messagebox.showerror("Error", "Not enough points to form a segment in one of the ROIs imported.")
            return

        self.update_color()
        
        segment_x_points = []
        segment_y_points = []

        for pair in coordinates:
            segment_x_points.append(pair[0])
            segment_y_points.append(pair[1])
            self.temp_ROI_points.append(self.axis.plot(segment_x_points, segment_y_points, self.marker_styles_point[self.id_color]))
        
        temp_segment = self.axis.plot(segment_x_points, segment_y_points, self.marker_styles_line[self.id_color])
        temp_points = self.temp_ROI_points[:]

        self.ROI_objects[self.ROI_index] = {
                'seg': temp_segment,
                'points': temp_points
                }
        self.update_ROI_visibility_list()
        self.canvas.draw()
        self.ROI_index += 1

    def process_segments(self):
        if len(self.segment_x_points) < 3:
            return  # At least 3 points needed to form a segment

        # Add the first point to the end to create a closed segment
        self.segment_x_points.append(self.segment_x_points[0])
        self.segment_y_points.append(self.segment_y_points[0])

        # Convert segment points to NumPy array
        segment_x_array = np.array(self.segment_x_points)
        segment_y_array = np.array(self.segment_y_points)

        # Draw the closed segment on the displayed image
        temp_segment = self.axis.plot(segment_x_array, segment_y_array, self.marker_styles_line[self.id_color])
        temp_points = self.temp_ROI_points[:]
        self.temp_ROI_points = []

        self.ROI_objects[self.ROI_index] = {
            'seg': temp_segment,
            'points': temp_points
        }
        self.ROI_index += 1
        self.update_ROI_visibility_list()
        self.canvas.draw()

        # Get coordinates of points inside the polygon
        self.list_in()

        # Calculate mean over time for the segment
        mean_values = self.mean_over_time()
        

        # Create a data structure with relevant information
        segment_data = {
            'segment_x_array': segment_x_array,
            'segment_y_array': segment_y_array,
            'mean_values': 
                        {
                        0: mean_values[0],
                        1: mean_values[1],
                    }
        }

        self.listes_graphs.append((segment_data['mean_values'][0]))#ajout canal vert
        self.listes_graphs.append((segment_data['mean_values'][1]))#ajout canal rouge
        # Pass the data to the DataViewer
        self.data_viewer.process_segment_data(segment_data)
        print('segmentation processed')
        self.update_displayed_image()
        dic=self.get_dic_ROI()


    def in_polygon(self, test):
        x, y = test
        nb_corners = len(self.segment_x_points)
        i, j = nb_corners - 1, nb_corners - 1
        odd_nodes = False
        for i in range(nb_corners):
            if (self.segment_y_points[i] < y and self.segment_y_points[j] >= y) or (self.segment_y_points[j] < y and self.segment_y_points[i] >= y):
                if (self.segment_x_points[i] + (y - self.segment_y_points[i]) / (self.segment_y_points[j] - self.segment_y_points[i]) * (self.segment_x_points[j] - self.segment_x_points[i]) < x):
                    odd_nodes = not odd_nodes
            j = i
        return odd_nodes
    
    def list_in(self):
        left = int(min(self.segment_x_points))  # Pixels inside the polygon are inside a known square
        right = int(max(self.segment_x_points))
        top = int(max(self.segment_y_points))
        bot = int(min(self.segment_y_points))
        res_x = []
        res_y = []
        for x in range(left, right, 1):
            for y in range(bot, top, 1):
                if self.in_polygon((x, y)):
                    res_x.append(x)
                    res_y.append(y)
        self.x_in=res_x
        self.y_in=res_y

    def mean(self,image):
        out = 0
        for i in range(0, len(self.x_in)):
            out += image[self.y_in[i]][self.x_in[i]]
        out = out / len(self.x_in)
        return out
    
    def mean_over_time(self): #Mean is calculated and then normalized
        try:
            # Lire toutes les images du fichier TIFF
            #images = imageio.volread(r'C:\Users\carlo\Downloads\transfer_6891262_files_d43c2e32\220728-S2_04_500mV.ome.tiff')
            #print("Nbr d'images :",(len(images[1])))# canal vert ou rouge, jsp
            # Initialiser une liste pour stocker les moyennes au fil du temps
            mean_values = [[],[]]
            images = self.original_image
            f0_green=0
            f0_red=0
            # Parcourir toutes les images et calculer la moyenne des valeurs des pixels
            for i in range(len(images[0])):#0= canal vert, 1=canal rouge
                mean_value_green = 2**16-self.mean(images[0][i])
                mean_value_red = 2**16-self.mean(images[1][i])
                mean_values[0].append(mean_value_green)
                mean_values[1].append(mean_value_red)
            ###NORMALIZATION###
            # for i in range (250): #Normalization : F0 is calculated over the first 250 images
            #     f0_green+=mean_values[0][i]
            #     f0_red+=mean_values[1][i]
            # f0_green=f0_green/250
            # f0_red=f0_red/250
            # for i in range (len(mean_values[0])):
            #     mean_values[0][i]=(mean_values[0][i]-f0_green)/f0_green
            #     mean_values[1][i]=(mean_values[1][i]-f0_red)/f0_red

                
            # for image in images[0]:#0= canal vert, 1=canal rouge
            #     mean_value = 2**16-self.mean(image)
            #     mean_values.append(mean_value)


            return mean_values

        except Exception as e:
            print("Error calculating mean over time:", e)
            return None
    
    def toggle_ROI_visibility(self, index, visibility):
        self.ROI_objects[index]['seg'][0].set_visible(visibility)
        if self.show_tags_var.get():
            self.display_tag(index+1)
        for points_list in self.ROI_objects[index]['points']:
            for point in points_list:
                point.set_visible(visibility)
        self.canvas.draw_idle()
            
    def update_color(self):
        if self.id_color<7:
            self.id_color+=1
        else : 
            self.id_color=0

    def update_ROI_visibility_list(self):
        self.GUI.update_ROI_visibility_list()
    
    def create_tag(self, id, x, y):
        tag_artist = self.axis.text(x, y, f"ROI {id}", color='white', fontsize=10, ha='center', va='center')
        self.tag_artists.append(tag_artist)
    
    def display_tag(self, id):
        if not self.ROI_objects[id-1]['seg'][0].get_visible():
            self.tag_artists[id-1].set_visible(False)
        else:
            self.tag_artists[id-1].set_visible(True)

    def remove_all_tags(self):
        for tag_artist in self.tag_artists:
            tag_artist.set_visible(False)

    def get_dic_ROI(self):
        return self.GUI.get_dic_ROI()
    
