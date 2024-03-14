#data_viewer.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, StringVar
import csv
import os

class DataViewer(ttk.Frame):
    def __init__(self, master, GUI=None):
        super().__init__(master)
        self.GUI = GUI

        self.ROI_data = {}
        self.selected_ROI_index = 0

        tree_frame = ttk.Frame(self)
        tree_frame.pack(side=tk.TOP, padx=10, pady=10)

        self.tree = ttk.Treeview(tree_frame, columns=('Index', 'Mean Intensity'), show='headings', selectmode='browse')
        self.tree.heading('#1', text='Index')
        self.tree.column('#1', width=50)  

        self.tree.heading('#2', text='Mean Intensity')
        self.tree.column('#2', width=100)  
        self.tree.pack(side=tk.LEFT)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill='y')

        self.tree.configure(yscroll=scrollbar.set)

        button_container = ttk.Frame(self)
        button_container.pack(side=tk.TOP, pady=10)

        self.selected_ROI_var = StringVar()
        self.ROI_combobox = ttk.Combobox(button_container, textvariable=self.selected_ROI_var)
        self.ROI_combobox.pack(side=tk.LEFT, padx=10)
        self.ROI_combobox.bind("<<ComboboxSelected>>", self.handle_combobox_selection)

        self.prev_button = ttk.Button(button_container, text="Previous", command=self.show_previous_page)
        self.prev_button.pack(side=tk.LEFT, padx=10)

        self.next_button = ttk.Button(button_container, text="Next", command=self.show_next_page)
        self.next_button.pack(side=tk.LEFT, padx=10)

        csv_buttons_frame = ttk.Frame(self)
        csv_buttons_frame.pack(side=tk.TOP, pady=10)

        self.load_button = ttk.Button(csv_buttons_frame, text="Load CSV", command=self.load_csv)
        self.load_button.pack(side=tk.LEFT, padx=10)

        self.save_button = ttk.Button(csv_buttons_frame, text="Save as CSV", command=self.save_as_csv)
        self.save_button.pack(side=tk.LEFT, padx=10)

        self.page_size = 50 
        self.current_page = {}
        self.total_pages = {} 

    def process_segment_data(self, segment_data):
        segment_x_array = segment_data['segment_x_array']
        segment_y_array = segment_data['segment_y_array']
        mean_values = segment_data['mean_values']

        coordinates = [(x, y) for x, y in zip(segment_x_array, segment_y_array)]
        means_data = (list(range(1, len(mean_values))), mean_values[:-1])

        if self.ROI_data == {}:
            next_index = 1
        else:
            next_index = max(self.ROI_data.keys()) + 1
        
        self.selected_ROI_index = next_index

        self.ROI_data[self.selected_ROI_index] = {'coord': coordinates, 'means': means_data}

        self.total_pages[self.selected_ROI_index] = (len(self.ROI_data[self.selected_ROI_index]['means'][1]) / self.page_size) + 1 
        self.current_page[self.selected_ROI_index] = 0 

        self.update_ROI_combobox()
        self.selected_ROI_var.set(self.selected_ROI_index)
        self.new_selection_display_data()
    
    def data_tree_clean_rebuild(self):
        self.tree.delete(*self.tree.get_children())
        self.tree.heading('#1', text='Index')
        self.tree.heading('#2', text='Mean Intensity')

    def new_selection_display_data(self):
        self.data_tree_clean_rebuild()
        self.display_data()

    def display_data(self):
        #self.data_tree_clean_rebuild()
        self.selected_ROI_index = int(self.selected_ROI_var.get())
        self.update_ROI_combobox()

        start_row = self.current_page[self.selected_ROI_index] * self.page_size
        end_row = start_row + self.page_size

        for i, (index, mean_intensity) in enumerate(zip(self.ROI_data[self.selected_ROI_index]['means'][0][start_row:end_row], self.ROI_data[self.selected_ROI_index]['means'][1][start_row:end_row]), start_row + 1):
            self.tree.insert('', 'end', values=[index, round(mean_intensity, 2)])

    def save_as_csv(self):
        project_path = self.get_project_path()
        file_path = os.path.join(project_path, "data_viewer_setup.csv")

        with open(file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            image_path = self.GUI.get_image_path()
            image_name = os.path.basename(image_path)
            csv_writer.writerow([f'Image-{image_name}'])
            temp_row = ['ROI', 'Coord', 'Intensity_Mean']
            csv_writer.writerow(temp_row)

            for roi_index, roi_data in self.ROI_data.items():
                row_data = [roi_index, str(roi_data['coord']), str(roi_data['means'][1])]
                csv_writer.writerow(row_data)

        messagebox.showinfo("Save Successful", f"Data saved to project folder.")

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])

        if file_path:
            try:
                with open(file_path, 'r') as csvfile:
                    csv_reader = csv.reader(csvfile)
                    header = next(csv_reader)
                    if header[0].startswith('Image-'):
                        if header[0] != f'Image-{os.path.basename(self.GUI.get_image_path())}':
                            raise ValueError("Data from different image")
                    else:
                        raise ValueError("Invalid CSV format")

                    data = [row for row in csv_reader]

                    self.process_data_from_csv(header, data)

                    messagebox.showinfo("Load Successful", f"Data loaded from {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Error loading data from {file_path}: {e}")

    def process_data_from_csv(self, header, data):
        # Remove the previous data
        self.data_tree_clean_rebuild()
        self.ROI_data = {}
        self.current_page = {}
        self.total_pages = {}

        # Process the new data
        for row in data:
            if row[0] != 'ROI':
                roi_index = int(row[0])
                coord = eval(row[1])
                means = eval(row[2])
                means = (list(range(1, len(means))), means[:-1])

                self.ROI_data[roi_index] = {'coord': coord, 
                                            'means': means }
                self.GUI.draw_segments_from_csv(coord)
                
                self.current_page[roi_index] = 0
                self.total_pages[roi_index] = (len(self.ROI_data[roi_index]['means'][1]) / self.page_size) + 1

        self.selected_ROI_index = 1
        self.update_ROI_combobox()
        self.display_data()

    def update_ROI_combobox(self):
        self.ROI_combobox['values'] = list(self.ROI_data.keys())
        self.ROI_combobox.set(self.selected_ROI_index)

    def handle_combobox_selection(self, event):
        self.selected_ROI_index = int(self.selected_ROI_var.get())
        self.new_selection_display_data()

    def show_previous_page(self):
        if self.current_page[self.selected_ROI_index] > 0:
            self.current_page[self.selected_ROI_index] -= 1
            self.new_selection_display_data()
    
    def show_next_page(self):
        if self.current_page[self.selected_ROI_index] < (self.total_pages[self.selected_ROI_index] - 1):
            self.current_page[self.selected_ROI_index] += 1
            self.new_selection_display_data()
    
    def get_project_path(self):
        return self.GUI.get_project_path()
