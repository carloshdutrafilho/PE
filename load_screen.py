from tkinter import Entry, Frame, Label, Button, ttk, filedialog
from ttkthemes import ThemedStyle
import os

class LoadScreen(Frame):
    def __init__(self, master=None, app=None, main_screen=None):  # Add main_screen parameter
        super().__init__(master)
        self.app = app
        self.main_screen = main_screen  # Reference to the MainScreen
        self.pack(expand=True, fill="both")

        # Frame para Load Image / Create Project
        self.load_frame = Frame(self)
        self.load_frame.pack(pady=10)

        # Entrada de texto para o nome do projeto (Create Project)
        self.entry_project_name = Entry(self.load_frame, width=30)
        self.entry_project_name.grid(row=0, column=0, padx=5, pady=5, columnspan=2)

        # Botão para Load Image (Create Project)
        self.b_load_image = ttk.Button(self.load_frame, text="Load Image", style="TButton", command=self.load_image)
        self.b_load_image.grid(row=1, column=0, padx=5, pady=5)

        # Label informativa (Load Image / Create Project)
        self.msg_load = Label(self.load_frame, text="Load Image (.tiff) / Create Project")
        self.msg_load["font"] = ("Verdana", "12", "bold")
        self.msg_load.grid(row=1, column=1, padx=5, pady=5)

        # Frame para Load Project
        self.load_project_frame = Frame(self)
        self.load_project_frame.pack(pady=10)

        # Botão para Load Project
        self.b_load_project = ttk.Button(self.load_project_frame, text="Load Project", style="TButton", command=self.load_project)
        self.b_load_project.grid(row=0, column=0, padx=5, pady=5)

        # Label informativa (Load Project)
        self.msg_load_project = Label(self.load_project_frame, text="Load Project")
        self.msg_load_project["font"] = ("Verdana", "12", "bold")
        self.msg_load_project.grid(row=0, column=1, padx=5, pady=5)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("TIFF files", "*.tiff;*.tif")])
        if file_path:
            self.image_viewer.load_image(file_path)
            self.update_recent_files(file_path)

    def create_project(self, project_name):
        if not self.validate_entry():
            self.quit()
            
        print(f"Creating project: {project_name}")
        # Access MainScreen and display the image
        self.main_screen.display_image(self.app.selected_file)

    def load_project(self):
        # Implemente a lógica para carregar o projeto
        print("Loading project...")
        
    def validate_entry(self):
        if not self.entry_project_name.get():
            self.quit()
