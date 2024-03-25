#data_viewer.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, StringVar, Toplevel
import csv
import os
import matplotlib.pyplot as plt 

class DataViewer(ttk.Frame):
    def __init__(self, master, GUI=None):
        super().__init__(master)
        self.GUI = GUI
        self.data_viewer = None

        self.ROI_data = {}
        self.selected_ROI_index = 0
        self.listes_graphs = []
        self.page_size = 50 
        self.current_page = {}
        self.total_pages = {} 

        tree_frame = ttk.Frame(self)
        tree_frame.pack(side=tk.TOP, padx=10, pady=10)

        self.tree = ttk.Treeview(tree_frame, columns=('Index', 'Mean Intensity Green','Mean Intensity Red'), show='headings', selectmode='browse')
        self.tree.heading('#1', text='Index')
        self.tree.column('#1', width=50)  

        self.tree.heading('#2', text='Mean Intensity Green')
        self.tree.column('#2', width=100)  

        self.tree.heading('#3', text='Mean Intensity Red')
        self.tree.column('#3', width=100)  
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
    
    def disable_functionalities_pre_load(self):
        self.prev_button.config(state='disabled')
        self.next_button.config(state='disabled')
        self.load_button.config(state='disabled')
        self.save_button.config(state='disabled')
        self.ROI_combobox.config(state='disabled')
    
    def enable_functionalities_post_load(self):
        self.prev_button.config(state='normal')
        self.next_button.config(state='normal')
        self.load_button.config(state='normal')
        self.save_button.config(state='normal')
        self.ROI_combobox.config(state='readonly')

    def process_segment_data(self, segment_data):
        segment_x_array = segment_data['segment_x_array']
        segment_y_array = segment_data['segment_y_array']
        mean_values_green = segment_data['mean_values'][0]
        mean_values_red= segment_data['mean_values'][1]
        coordinates = [(x, y) for x, y in zip(segment_x_array, segment_y_array)]
        means_data = (list(range(1, len(mean_values_green))), mean_values_green[:-1],mean_values_red[:-1])

        if self.ROI_data == {}:
            self.selected_ROI_index = 1
        else:
            self.selected_ROI_index = max(self.ROI_data.keys()) + 1

        self.ROI_data[self.selected_ROI_index] = {
            'coord': coordinates, 
            'means': {
            0: mean_values_green,
            1: mean_values_red
            }
        }


        self.total_pages[self.selected_ROI_index] = (len(self.ROI_data[self.selected_ROI_index]['means'][1]) / self.page_size) + 1 
        self.current_page[self.selected_ROI_index] = 0 

        self.update_ROI_combobox()
        self.selected_ROI_var.set(self.selected_ROI_index)
        self.generate_graphs()
        self.new_selection_display_data()
        
    def data_tree_clean_rebuild(self):
        self.tree.delete(*self.tree.get_children())
        self.tree.heading('#1', text='Index')
        self.tree.heading('#2', text='Mean Intensity Green')
        self.tree.heading('#3', text='Mean Intensity Red') 

    def new_selection_display_data(self):
        self.data_tree_clean_rebuild()
        self.display_data()

    def display_data(self):
        #self.data_tree_clean_rebuild()
        self.selected_ROI_index = int(self.selected_ROI_var.get())
        self.update_ROI_combobox()

        start_row = self.current_page[self.selected_ROI_index] * self.page_size
        end_row = start_row + self.page_size

        # Récupérer les données pour les deux canaux
        mean_values_green = self.ROI_data[self.selected_ROI_index]['means'][0]
        mean_values_red = self.ROI_data[self.selected_ROI_index]['means'][1]

        # Récupérer les valeurs de l'intensité moyenne pour les deux canaux
        mean_intensities_green = mean_values_green[start_row:end_row]
        mean_intensities_red = mean_values_red[start_row:end_row]   

        for i, (index, mean_intensity_green, mean_intensity_red) in enumerate(zip(range(start_row, end_row), mean_intensities_green, mean_intensities_red), start=start_row + 1):
                self.tree.insert('', 'end', values=[index, round(mean_intensity_green, 2), round(mean_intensity_red, 2)])

    def save_as_csv(self):
        project_path = self.get_project_path()
        file_path = os.path.join(project_path, "data_viewer_setup.csv")

        with open(file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            image_path = self.GUI.get_image_path()
            image_name = os.path.basename(image_path)
            csv_writer.writerow([f'Image-{image_name}'])
            temp_row = ['ROI', 'Coord', 'Intensity_Mean_Green','Intensity_Mean_Red']
            csv_writer.writerow(temp_row)

            for roi_index, roi_data in self.ROI_data.items():
                row_data = [roi_index, str(roi_data['coord']), str(roi_data['means'][0]),str(roi_data['means'][1])]
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
        self.GUI.reset_context_for_segments_csv()
        print('Taille Data:',len(data))
        # Process the new data
        for row in data:
            if row[0] != 'ROI':
                roi_index = int(row[0])
                coord = eval(row[1])
                means_green = eval(row[2])
                means_red=eval(row[3])
                
                means = (list(range(1, len(means))), means[:-1])

                next_index = 1
                if len(self.ROI_data) != 0:
                    next_index = max(self.ROI_data.keys()) + 1

                mean_values_green = means[0]
                mean_values_red = means[1]
                means_green = (list(range(1, len(mean_values_green))), mean_values_green[:-1])
                means_red = (list(range(1, len(mean_values_red))), mean_values_red[:-1])

                self.ROI_data[next_index] = {
                'coord': coord,
                'means': {
                    0: means_green,  # Canal vert
                    1: means_red     # Canal rouge
                }
                }
                self.GUI.draw_segments_from_csv(coord)
                # self.listes_graphs.append((self.ROI_data[roi_index]['means'][1]))
                # self.graph_viewer.process_to_graph(list(range(0, len(self.listes_graphs[0]))),self.listes_graphs)

                self.current_page[next_index] = 0
                self.total_pages[next_index] = (len(self.ROI_data[next_index]['means'][1]) / self.page_size) + 1
                self.selected_ROI_index = next_index
            
        self.update_ROI_combobox()
        self.display_data()
        self.generate_graphs()
    
    def generate_graphs(self):
        
        self.graph_viewer.set_ROI_data(self.ROI_data)
        self.graph_viewer.update_displayed_ROI(self.selected_ROI_index)
        self.graph_viewer.process_to_graph(channel=0)  # Afficher le graphique pour le canal vert
        self.graph_viewer.process_to_graph(channel=1)
         
        #self.graph_viewer.clean_graph()

    def update_ROI_combobox(self):
        self.ROI_combobox['values'] = list(self.ROI_data.keys())
        self.ROI_combobox.set(self.selected_ROI_index)

    def handle_combobox_selection(self, event):
        self.selected_ROI_index = int(self.selected_ROI_var.get())
        self.new_selection_display_data()
        self.graph_viewer.update_displayed_ROI(self.selected_ROI_index)

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

    def set_graph_viewer(self, graph_viewer):
        self.graph_viewer = graph_viewer

    def get_dic_ROI(self):
        return self.ROI_data
