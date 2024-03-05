import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GraphViewer(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        # Create a matplotlib figure and axis
        self.figure, self.axis = Figure(figsize=(4, 2), tight_layout=True), None
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Example: Create a simple line plot
        self.plot_data()

    def plot_data(self):
        if self.axis is None:
            # Create axis if not already created
            self.axis = self.figure.add_subplot(111)

        # Example data (replace this with your own data)
        x_data = [1, 2, 3, 4, 5]
        y_data = [10, 5, 8, 12, 6]

        # Clear previous plot and plot new data
        self.axis.clear()
        self.axis.plot(x_data, y_data, marker='o', linestyle='-')

        # Set labels and title
        self.axis.set_xlabel('X-axis Label')
        self.axis.set_ylabel('Y-axis Label')
        self.axis.set_title('Graph Viewer')

        # Redraw canvas
        self.canvas.draw()
