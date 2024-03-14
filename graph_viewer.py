import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv
import ast  

class GraphViewer(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.image_container = tk.Frame(self)
        self.image_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create a matplotlib figure and axis
        self.figure, self.axis = Figure(figsize=(4, 2), tight_layout=True), None
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.color_mode = 'grayscale'
        # self.plot_button = tk.Button(self.image_container, text="Plot graph", command=lambda: self.plot_data('dataset2.csv'))
        # self.plot_button.pack(side=tk.TOP, anchor=tk.SW, padx=10, pady=10)
        self.is_color_changed = False
        self.checkboxes = []
        self.datasets_visibility = []
        for i in range(3):  # Change 3 to the number of datasets
            visibility_var = tk.BooleanVar(value=True)  # Checkbox variable to track visibility
            checkbox = ttk.Checkbutton(self.image_container, text=f"ROI {i+1}", variable=visibility_var,
                                       command=lambda idx=i: self.toggle_dataset(idx))
            checkbox.pack(side=tk.BOTTOM)
            self.checkboxes.append(checkbox)
            self.datasets_visibility.append(visibility_var)

    # def plot_data(self):
    #     if self.axis is None:
    #         # Create axis if not already created
    #         self.axis = self.figure.add_subplot(111)

    #     # Example data (replace this with your own data)
    #     x_data = [1, 2, 3, 4, 5]
    #     y_data = [10, 5, 8, 12, 6]

    #     # Clear previous plot and plot new data
    #     self.axis.clear()
    #     self.axis.plot(x_data, y_data, marker='o', linestyle='-')

    #     # Set labels and title
    #     self.axis.set_xlabel('X-axis Label')
    #     self.axis.set_ylabel('Y-axis Label')
    #     self.axis.set_title('Graph Viewer')

    #     # Redraw canvas
    #     self.canvas.draw()


    def plot_data(self, csv_file='datatest2.csv'):
        if self.axis is None:
            # Create axis if not already created
            self.axis = self.figure.add_subplot(111)

        # Load data from CSV file
        x_data = []
        y_data = []
        try:
            with open(csv_file, mode='r') as file:
                reader = csv.reader(file)
                x_data_str = next(reader, [])  # Get the first row as string
                y_data_str = next(reader, [])  # Get the second row as string

                # Parse the strings to lists
                x_data = ast.literal_eval(x_data_str[0])
                y_data = ast.literal_eval(y_data_str[0])
                
                # Convert values to float if possible
                x_data = [float(x) for x in x_data if isinstance(x, (int, float))]
                y_data = [float(y) for y in y_data if isinstance(y, (int, float))]

        except FileNotFoundError:
            print(f"Error: File '{csv_file}' not found.")
            return
        except Exception as e:
            print(f"Error: Unable to read data from '{csv_file}': {e}")
            return

        # Plot data
        self.axis.clear()
        self.axis.plot(x_data, y_data, linestyle='-')  # Tracer une courbe lisse sans marqueurs

        # Set labels and title
        self.axis.set_xlabel('X-axis Label')
        self.axis.set_ylabel('Y-axis Label')
        self.axis.set_title('Graph Viewer')
        self.axis.set_xlim([0, 1000])  # Example: set x-axis limits from 0 to 10
        self.axis.set_ylim([64000, 65000]) 
        # Redraw canvas
        self.canvas.draw()

    def toggle_dataset(self, index):
        # Toggle the visibility of the dataset corresponding to the given index
        if self.axis is not None:
            lines = self.axis.lines
            if index < len(lines):
                line = lines[index]
                line.set_visible(self.datasets_visibility[index].get())  # Get visibility from checkbox variable
                self.canvas.draw()



    def process_to_graph(self, x_data=None, y_data_list=None):
        if self.axis is None:
            # Create axis if not already created
            self.axis = self.figure.add_subplot(111)

        if x_data is None or y_data_list is None:
            print("Error: Both x_data and y_data_list must be provided.")
            return

        # Check if the provided data are lists
        if not isinstance(x_data, list) or not isinstance(y_data_list, list):
            print("Error: Both x_data and y_data_list must be provided as lists.")
            return

        try:
            # Convert values to float if possible
            x_data = [float(x) for x in x_data if isinstance(x, (int, float))]

            # Convert each sublist in y_data_list to floats if possible
            y_data_list = [[float(y) for y in sublist if isinstance(y, (int, float))] for sublist in y_data_list]

        except Exception as e:
            print(f"Error: Unable to process data: {e}")
            return

        # Define colors for plotting
        colors = ['b-', 'g-', 'r-', 'c-', 'm-', 'y-', 'k-', 'w-']

        # Plot data
        self.axis.clear()
        for i, (y_data, visibility_var) in enumerate(zip(y_data_list, self.datasets_visibility)):
            color = colors[i % len(colors)]  # Cycle through colors if there are more than 8 datasets
            if visibility_var.get():  # Check if dataset is visible
                self.axis.plot(x_data, y_data, color, label=f'Dataset {i+1}')

        # Set labels and title
        self.axis.set_xlabel('X-axis Label')
        self.axis.set_ylabel('Y-axis Label')
        self.axis.set_title('Graph Viewer')
        self.axis.set_xlim([0, 1000])  # Example: set x-axis limits from 0 to 10
        self.axis.set_ylim([64000, 65000]) 
        self.axis.legend()  # Add legend

        # Redraw canvas
        self.canvas.draw()
