import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.widgets import Slider
import numpy as np

class ImageSliderApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        # Create a numpy array of images (150, 300, 300) for demonstration
        self.images = np.random.rand(150, 300, 300)

        # Create a Matplotlib figure and axis
        self.figure = Figure(figsize=(6, 6))
        self.axis = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Display the first image
        self.current_index = 0
        self.image_display = self.axis.imshow(self.images[self.current_index], cmap='gray')

        # Add a slider to scroll through images
        ax_slider = self.figure.add_axes([0.2, 0.05, 0.65, 0.03])
        self.slider = Slider(ax_slider, 'Image', 0, 149, valinit=0)
        self.slider.on_changed(self.update_image)

    def update_image(self, value):
        index = int(self.slider.val)
        self.image_display.set_data(self.images[index])
        self.canvas.draw_idle()