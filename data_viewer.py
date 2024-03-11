import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
import os

class DataViewer(ttk.Frame):
    def __init__(self, master, GUI=None):
        super().__init__(master)
        self.GUI = GUI

        self.ROI_data = None
        self.selected_ROI_index = 0

        self.tree = ttk.Treeview(self, columns=('Index', 'Mean Intensity'), show='headings', selectmode='browse')

        self.tree.heading('#1', text='Index')
        self.tree.column('#1', width=50)  # Defina a largura desejada para a coluna 'Index'

        self.tree.heading('#2', text='Mean Intensity')
        self.tree.column('#2', width=100)  # Defina a largura desejada para a coluna 'Mean Intensity'

        self.tree.pack(side=tk.TOP, padx=10, pady=10)  # Mude para TOP para colocar a tabela no topo

        # Adicione uma barra de rolagem vertical
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill='y')

        self.tree.configure(yscroll=scrollbar.set)

        # Adicione os botões Save e Load centralizados
        button_container = ttk.Frame(self)
        button_container.pack(side=tk.TOP, pady=10)

        self.save_button = ttk.Button(button_container, text="Save as CSV", command=self.save_as_csv)
        self.save_button.pack(side=tk.LEFT, padx=10)

        self.load_button = ttk.Button(button_container, text="Load CSV", command=self.load_csv)
        self.load_button.pack(side=tk.LEFT, padx=10)

        # Adicione os botões de navegação
        self.prev_button = ttk.Button(button_container, text="Previous Page", command=self.show_previous_page)
        self.prev_button.pack(side=tk.LEFT, padx=10)

        self.next_button = ttk.Button(button_container, text="Next Page", command=self.show_next_page)
        self.next_button.pack(side=tk.LEFT, padx=10)

        self.page_size = 50  # Número de linhas a serem exibidas por página
        self.current_page = 0
        self.total_pages = 0  # Inicialize com zero

    def get_project_path(self):
        return self.GUI.get_project_path()

    def process_segment_data(self, segment_data):
        # Extract relevant information from the segment data

        segment_x_array = segment_data['segment_x_array']
        segment_y_array = segment_data['segment_y_array']
        mean_values = segment_data['mean_values']

        # Convert x and y arrays to a list of coordinate pairs
        coordinates = [(x, y) for x, y in zip(segment_x_array, segment_y_array)]

        # Display the segment data in the table
        means_data = (list(range(1, len(mean_values))), mean_values[:-1])

        # Atualize o número total de páginas
        self.total_pages = len(mean_values) // self.page_size + 1

        if (self.ROI_data is None):
            next_index = 1
        else:
            next_index = max(self.ROI_data.keys()) + 1
        self.selected_ROI_index = next_index
        self.ROI_data = { next_index : { 'coord' : coordinates,
                                         'means' : means_data } }

        self.display_data()
    
    def data_tree_clean_rebuild(self):
        self.tree.delete(*self.tree.get_children())
        self.tree.heading('#1', text='Index')
        self.tree.heading('#2', text='Mean Intensity')

    def display_data(self):
        self.data_tree_clean_rebuild()

        start_row = self.current_page * self.page_size
        end_row = start_row + self.page_size

        for i, (index, mean_intensity) in enumerate(zip(self.ROI_data[self.selected_ROI_index]['means'][0][start_row:end_row], self.ROI_data[self.selected_ROI_index]['means'][1][start_row:end_row]), start_row + 1):
            self.tree.insert('', 'end', values=[index, round(mean_intensity, 2)])

    def save_as_csv(self):
        project_path = self.get_project_path()
        file_path = os.path.join(project_path, "data_viewer_setup.csv")

        with open(file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['ROI', 'Coord', 'Intensity_Mean'])

            for roi_index, roi_data in self.ROI_data.items():
                # Concatenate all elements into a single list
                row_data = [roi_index, str(roi_data['coord']), str(roi_data['means'][1])]

                # Write the row to the CSV file
                csv_writer.writerow(row_data)

        messagebox.showinfo("Save Successful", f"Data saved to project folder.")




    def load_csv(self):
        # Ask user for a file to open
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])

        if file_path:
            try:
                # Read data from the CSV file
                with open(file_path, 'r') as csvfile:
                    csv_reader = csv.reader(csvfile)
                    header = next(csv_reader)  # Skip header
                    data = [row for row in csv_reader]

                # Update the displayed data in the table
                self.update_data_display([], data)
                messagebox.showinfo("Load Successful", f"Data loaded from {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Error loading data from {file_path}: {e}")

    def show_previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.display_data()
    
    def show_next_page(self):
        if self.current_page < (self.total_pages - 1):
            self.current_page += 1
            self.display_data()
