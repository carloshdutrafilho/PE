# GUI.py
from tkinter import ttk
import tkinter.messagebox
import datetime
import tkinter as tk
from tkinter import OptionMenu, StringVar, filedialog
from image_viewer import ImageViewer
from data_viewer import DataViewer  
from graph_viewer import GraphViewer
from file_viewer import FileViewer
from load_screen import LoadScreen

class GUI(tk.Toplevel):
    def __init__(self, master=None, app=None, image_path=None):
        super().__init__(master)
        self.title("Main Screen")
        self.geometry("1200x800")
        self.configure(bg='white')
        
        # Initialize image viewer
        self.image_viewer = None
        
        # Container for File Explorer, Image Viewer, and Data/Graph Viewers
        main_container = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashwidth=5, sashrelief=tk.SUNKEN)
        main_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.msg = tk.Label(main_container, text="Main Screen")
        self.msg["font"] = ("Verdana", "12", "bold")
        #self.msg.pack()
        #main_container.add(self.msg, minsize=100)  # Set minimum size

        # Project path
        self.project_path = None
        
        # File Explorer
        file_explorer_frame = FileViewer(main_container, image_viewer=self.image_viewer)
        #file_explorer_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        main_container.add(file_explorer_frame, minsize=100)  # Set minimum size
        
        #Image Viewer
        self.image_viewer = ImageViewer(main_container,self)
        #self.image_viewer.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        main_container.add(self.image_viewer, minsize=200)  # Set minimum size
        self.image_viewer.disable_functionalities_pre_load()

        # Data and Graph Viewers
        data_graph_frame = tk.PanedWindow(main_container, orient=tk.VERTICAL, sashwidth=8, sashrelief=tk.SUNKEN)
        main_container.add(data_graph_frame, minsize=200)  # Set minimum size

        # Data Viewer
        self.data_viewer = DataViewer(data_graph_frame, self)
        self.image_viewer.set_data_viewer(self.data_viewer)
        data_graph_frame.add(self.data_viewer, minsize=200)  # Set minimum size
        self.data_viewer.disable_functionalities_pre_load()

        # Graph Viewer
        self.graph_viewer = GraphViewer(data_graph_frame)
        self.graph_viewer.disable_functionalities_pre_load()
        self.image_viewer.set_graph_viewer(self.graph_viewer)
        self.data_viewer.set_graph_viewer(self.graph_viewer)
        data_graph_frame.add(self.graph_viewer, minsize=200)  # Set minimum size
        
        self.load_screen = LoadScreen(self.master, app=self, image_viewer=self.image_viewer)
        
        # Create a menu bar
        self.menubar = tk.Menu(self)
        self.master.config(menu=self.menubar)
        
        # File menu
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.file_menu)

        # Open File submenu
        self.open_file_menu = tk.Menu(self.file_menu, tearoff=0)
        self.file_menu.add_cascade(label="Open File", menu=self.open_file_menu)
        self.open_file_menu.add_command(label="Open CSV", command=lambda: self.open_specific_file("csv"))
        self.open_file_menu.add_command(label="Open TIFF", command=lambda: self.open_specific_file("tiff"))

        # Open Recent menu
        self.open_recent_menu = tk.Menu(self.file_menu, tearoff=0)
        self.file_menu.add_cascade(label="Open Recent", menu=self.open_recent_menu)

        self.file_menu.add_separator()
        self.file_menu.add_command(label="Save", accelerator="Ctrl+S", command=self.save)
        self.file_menu.add_command(label="Save As...", accelerator="Ctrl+Shift+S", command=self.save_as)
        self.file_menu.add_command(label="Save All", accelerator="Ctrl+K", command=self.save_all)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", accelerator="Ctrl+E", command=self.quit_software)

        # # Store the file_menu as an instance variable
        # self.file_menu = file_menu
        
        # Edit menu
        self.edit_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edit", menu=self.edit_menu)
        
        # Preferences menu
        self.preferences_menu = tk.Menu(self.menubar, tearoff=0)
        self.preferences_menu.add_command(label="Mode", command=self.show_preferences)
        self.menubar.add_cascade(label="Preferences", menu=self.preferences_menu)
        
        # Help menu
        self.help_menu = tk.Menu(self.menubar, tearoff=0)
        self.help_menu.add_command(label="About", command=self.show_about)
        self.menubar.add_cascade(label="Help", menu=self.help_menu)

        self.config(menu=self.menubar)
    
        # Variable to track night mode
        self.night_mode = tk.BooleanVar()
        self.night_mode.set(False)
        
        # Bind shortcut keys
        self.bind_shortcuts()
        
        # List to store recently used files
        self.recent_files = [] 
        self.protocol("WM_DELETE_WINDOW", self.quit_software)
    
            # Adicione o menu "View"
        self.view_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="View", menu=self.view_menu)

        # Adicione uma subopção para segmentações ROI
        self.roi_menu = tk.Menu(self.view_menu, tearoff=0)
        self.view_menu.add_cascade(label="ROI Segmentations", menu=self.roi_menu)

        # Adicione itens de menu para cada segmentação ROI
        self.roi_visibility_vars = []  # Variáveis para rastrear a visibilidade de cada ROI
    
    def update_ROI_visibility_list(self):
        self.roi_visibility_vars.clear()
        self.roi_menu.delete(0, tk.END)  
        for i in range(len(self.image_viewer.ROI_objects)):
            visibility_var = tk.BooleanVar(value=True)
            if (not self.image_viewer.ROI_objects[i]['seg'][0].get_visible()):
                visibility_var = tk.BooleanVar(value=False)
            self.roi_visibility_vars.append(visibility_var)
            self.roi_menu.add_checkbutton(label=f"ROI {i+1}", variable=visibility_var,
                                     command=lambda index=i: self.toggle_roi_visibility(index))

    def toggle_roi_visibility(self, index):
        # Toggle the visibility of ROI at given index
        visibility = self.roi_visibility_vars[index].get()
        self.image_viewer.toggle_ROI_visibility(index, visibility)

    def quit_software(self):
        self.quit()
    
    def enable_functionalities_post_load(self):
        self.image_viewer.enable_functionalities_post_load()
        self.data_viewer.enable_functionalities_post_load()
        self.graph_viewer.enable_functionalities_post_load()

    def get_project_path(self):
        return self.load_screen.get_project_path()
    
    def get_dic_ROI(self):
        return self.data_viewer.get_dic_ROI()
    
    def get_image_path(self):
        return self.load_screen.get_image_path()
    
    def draw_segments_from_csv(self, coordinates):
        self.image_viewer.draw_segments_from_csv(coordinates)

    def reset_context_for_segments_csv(self):
        self.image_viewer.reset_context_for_segments_csv()

    def bind_shortcuts(self):
        self.bind("<Control-U>", lambda event: self.open_file())
        self.bind("<Control-N>", lambda event: self.new_window())
        self.bind("<Control-S>", lambda event: self.save())
        self.bind("<Control-Shift-S>", lambda event: self.save_as())
        self.bind("<Control-K>", lambda event: self.save_all())
        self.bind("<Alt-F4>", lambda event: self.close_window())
        self.bind("<Control-E>", lambda event: self.quit())
        self.bind("<Control-R>", lambda event: self.open_recent_file(self.recent_files[0]) if self.recent_files else None)
        
    def open_specific_file(self, file_type):
        file_extension = "*.csv" if file_type == "csv" else "*.tiff"
        file_path = filedialog.askopenfilename(filetypes=[(f"{file_type.upper()} Files", file_extension)])
        if file_path:
            if file_type == "csv":
                self.data_viewer.load_csv(file_path)
            else:
                self.clean_display_seg_data()
                self.image_viewer.load_image(file_path)
            with open(self.load_screen.identification_file_path, "w") as identification_file:
                identification_file.write(f"\nPath-{self.load_screen.selected_file}")
    
    def clean_display_seg_data(self):
        self.data_viewer.clean_seg_data()
        self.image_viewer.clean_display_seg()
            
    def update_recent_files(self, file_path):
        # Update the list of recent files
        if file_path in self.recent_files:
            self.recent_files.remove(file_path)
        self.recent_files.insert(0, file_path)

        # Keep only the five most recent files
        self.recent_files = self.recent_files[:5]
    
        # Update the "Open Recent" menu
        self.update_open_recent_menu()
        
    def update_open_recent_menu(self):
        # Clear the current menu items
        self.open_recent_menu.delete(0, tk.END)

        # Add the recent files to the menu
        for i, file_path in enumerate(self.recent_files):
            accelerator = f"Ctrl+{i + 1}" if i < 9 else ""  # You can customize the accelerator
            self.open_recent_menu.add_command(
                label=f"Recent File {i + 1}",
                accelerator=accelerator,
                command=lambda path=file_path: self.open_recent_file(path)
            )
            
    def open_recent_file(self, file_path):
        self.image_viewer.load_image(file_path)
        self.update_recent_files(file_path)
    
    
    def show_preferences(self):
        # Create a preferences dialog with a night mode toggle
        preferences_dialog = tk.Toplevel(self)
        preferences_dialog.title("Mode")

        night_mode_checkbox = tk.Checkbutton(preferences_dialog, text="Night Mode",
                                             variable=self.night_mode, command=self.toggle_night_mode)
        night_mode_checkbox.pack(padx=10, pady=10)

    def toggle_night_mode(self):
        # Toggle night mode
        if self.night_mode.get():
            self.configure(bg='black')
            self.image_viewer.configure(bg='black')
            self.data_viewer.configure(bg='black')
            self.graph_frame.configure(bg='black')
        else:
            self.configure(bg='white')
            self.image_viewer.configure(bg='white')
            self.data_viewer.configure(bg='white')
            self.graph_frame.configure(bg='white')

    def new_window(self):
        # Implement the logic for opening a new window
        pass

    def save(self):
        # Implement the logic for saving
        pass

    def save_as(self):
        # Implement the logic for save as
        pass

    def save_all(self):
        # Implement the logic for saving all
        pass
    
    def show_about(self):
        about_info = (
            "Image Analysis Interface\n\n"
            "Author: Aya, Carlos, Marc, Tom\n"
            "Version: 1.0\n"
            f"Date: {datetime.date.today()}\n"
            "Copyright © 2024 PE BMD. All rights reserved."
        )

        tkinter.messagebox.showinfo("About", about_info)

# def main():
#     gui = GUI()
#     gui.mainloop()

# if __name__ == "__main__":
#     main()