import tkinter as tk
from tkinter import ttk

class DataViewer(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Add widgets for displaying data and creating graphs
        # (You can use Matplotlib for creating the graph)

        # Add widgets for displaying data and creating graphs
        self.data_text = tk.Text(self, wrap=tk.WORD, width=30, height=20)
        self.data_text.pack(side=tk.LEFT, padx=10, pady=10)

        self.save_button = tk.Button(self, text="Save as CSV", command=self.save_as_csv)
        self.save_button.pack(side=tk.LEFT, padx=10, pady=10)

    def update_data(self, data):
        # Update the displayed data in the text widget
        self.data_text.delete(1.0, tk.END)
        self.data_text.insert(tk.END, data)

    def save_as_csv(self):
        # Implement the code to save data as a CSV file
        pass