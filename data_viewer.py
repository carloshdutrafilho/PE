import tkinter as tk
from tkinter import ttk
import csv

class DataViewer(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Add widgets for displaying data as a table
        self.tree = ttk.Treeview(self, columns=('Column 1', 'Column 2'), show='headings', selectmode='browse')

        self.tree.heading('#1', text='Column 1')
        self.tree.heading('#2', text='Column 2')

        self.tree.pack(side=tk.LEFT, padx=10, pady=10)

        # Add vertical scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        print("This point is reached")

        self.tree.configure(yscroll=scrollbar.set)

        self.save_button = ttk.Button(self, text="Save as CSV", command=self.save_as_csv)
        self.save_button.pack(side=tk.LEFT, padx=10, pady=10)

    def update_data(self, data):
        # Update the displayed data in the table
        self.tree.delete(*self.tree.get_children())
        for row in data:
            self.tree.insert('', 'end', values=row)

    def save_as_csv(self):
        # Get data from the table
        data = [self.tree.item(item, 'values') for item in self.tree.get_children()]

        # Ask user for a file name and location
        file_path = tk.filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

        if file_path:
            # Write data to the CSV file
            with open(file_path, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['Column 1', 'Column 2'])  # Write header
                csv_writer.writerows(data)

            tk.messagebox.showinfo("Save Successful", f"Data saved to {file_path}")