import tkinter as tk
from tkinter import messagebox, ttk, Toplevel
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt 
import csv
import ast  

class GraphViewer(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        # Data structures
        self.ROI_data = {}
        self.selected_ROI_index = 1
        self.colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
        self.selected_color = ''

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
    
        self.compare_button = ttk.Button(self, text="Compare ROIs", command=self.compare_ROIs)
        self.compare_button.pack(side=tk.TOP, padx=10, pady=10)
    
    def disable_functionalities_pre_load(self):
        self.compare_button.config(state="disabled")

    def enable_functionalities_post_load(self):
        self.compare_button.config(state="normal")

    def compare_ROIs(self):
        if len(self.ROI_data) < 2:
            messagebox.showinfo("Error", "There must be at least two ROIs available for comparison.")
            return

        compare_window = Toplevel(self)
        compare_window.title("Compare ROIs")
        compare_window.geometry("600x400")

        fig, ax = plt.subplots() 

        def plot_comparison(selected_ROIs):
            ax.clear() 

            for ROI_index in selected_ROIs:
                if ROI_index in self.ROI_data:
                    x_data = self.ROI_data[ROI_index]['means'][0]
                    y_data = self.ROI_data[ROI_index]['means'][1]
                    x_data = [float(x) for x in x_data if isinstance(x, (int, float))]
                    y_data = [float(y) for y in y_data if isinstance(y, (int, float))]

                    ax.plot(x_data, y_data, label=f'ROI {ROI_index}')

            compare_window.destroy() 
            ax.set_xlabel('Time')
            ax.set_ylabel('Mean Intensity')
            ax.set_title('ROI Comparison')
            ax.legend()
            plt.show()

        def add_combobox():
            if len(comboboxes) < len(self.ROI_data):
                combobox = ttk.Combobox(compare_window, values=list(self.ROI_data.keys()), state="readonly")
                combobox.grid(row=len(comboboxes), column=0, padx=5, pady=5)
                comboboxes.append(combobox)
            else:
                messagebox.showinfo("Error", "You have already added all available ROIs. Add more ROIs to be able to compare more.")

        comboboxes = []
        add_combobox()
        add_combobox()

        compare_button = ttk.Button(compare_window, text="Compare", command=lambda: plot_comparison([int(combobox.get()) for combobox in comboboxes if combobox.get()]))
        compare_button.grid(row=len(comboboxes), column=1, padx=5, pady=5)

        add_button = ttk.Button(compare_window, text="+", command=add_combobox)
        add_button.grid(row=0, column=1, padx=5, pady=5)

    def toggle_dataset(self, index):
        # Toggle the visibility of the dataset corresponding to the given index
        if self.axis is not None:
            lines = self.axis.lines
            if index < len(lines):
                line = lines[index]
                line.set_visible(self.datasets_visibility[index].get())  # Get visibility from checkbox variable
                self.canvas.draw()

    def set_ROI_data(self, ROI_dict):
        self.ROI_data = ROI_dict
    
    def update_displayed_ROI(self, ROI_index):
        self.selected_ROI_index = ROI_index
        self.process_to_graph()

    def select_color(self):
        self.selected_color = self.colors[self.selected_ROI_index-1]

    def process_to_graph(self):
        if self.axis is None:
            self.axis = self.figure.add_subplot(111)

        if not self.ROI_data:
            print("Error: No ROI data available.")
            return

        if self.selected_ROI_index not in self.ROI_data:
            print(f"Error: ROI {self.selected_ROI_index} not found in ROI data.")
            return

        try:
            x_data = self.ROI_data[self.selected_ROI_index]['means'][0]
            y_data = self.ROI_data[self.selected_ROI_index]['means'][1]

            x_data = [float(x) for x in x_data if isinstance(x, (int, float))]
            y_data = [float(y) for y in y_data if isinstance(y, (int, float))]

            self.axis.clear()

            self.select_color()

            self.axis.plot(x_data, y_data, color=self.selected_color, linestyle='-', label=f'ROI {self.selected_ROI_index}')

            self.axis.set_xlabel('Time')
            self.axis.set_ylabel('Mean Intensity')
            self.axis.set_title('Graph Viewer')

            self.axis.set_xlim([0, 1000]) 
            self.axis.set_ylim([1000, 2000]) 
            
            # Redesenha o gráfico
            self.canvas.draw()

        except Exception as e:
            print(f"Error: Unable to process data: {e}")

    # def add_list_to_graph(self, new_list):
    #     print('rentrer dans add_list')
    #     self.list_graph.append(new_list)
    #     visibility_var = tk.BooleanVar(value=True)
    #     self.datasets_visibility.append(visibility_var)

    # def create_roi_checkboxes(self):
    #     for i in range(len(self.list_graph)):
    #         visibility_var = self.datasets_visibility[i]
            
    #         # Vérifier si le bouton ROI pour cet index existe déjà
    #         if i < len(self.checkboxes):
    #             self.checkboxes[i].config(variable=visibility_var)  # Mettre à jour la variable du bouton existant
    #         else:
    #             checkbox = ttk.Checkbutton(self.image_container, text=f"ROI {i+1}", variable=visibility_var,
    #                                     command=lambda idx=i: self.toggle_dataset(idx))
    #             checkbox.pack(side=tk.BOTTOM)
    #             self.checkboxes.append(checkbox)

    # for i, (y_data, visibility_var) in enumerate(zip(y_data_list, self.datasets_visibility)):
    #         color = colors[i % len(colors)]  # Cycle through colors if there are more than 8 datasets
    #         if visibility_var.get():  # Check if dataset is visible
    #             self.axis.plot(x_data, y_data, color, label=f'ROI {i+1}')