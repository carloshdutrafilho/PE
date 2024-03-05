from tkinter import Entry, Frame, Label, Button, ttk, filedialog
from ttkthemes import ThemedStyle
import os

class LoadScreen(Frame):
    def __init__(self, master=None, app=None, main_screen=None):  # Add main_screen parameter
        super().__init__(master)
        self.app = app
        self.main_screen = main_screen  # Reference to the MainScreen
        self.pack(expand=True, fill="both")

        # Configurando o título da janela
        self.master.title("Project Manager")

        # Ajustando o tamanho inicial da janela
        self.master.geometry("335x250")  # Substitua pelos valores desejados

        # Frame principal
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(expand=True, fill="both")

        # Frame para Load Image / Create Project
        self.load_frame = ttk.Frame(self.main_frame, relief="ridge")
        self.load_frame.grid(row=0, column=0, pady=10, sticky="nsew")

        # Etiqueta para Nome do Projeto
        self.label_project_name = Label(self.load_frame, text="Project Name: ", font=("Calibri", 10, "bold"))
        self.label_project_name.grid(row=1, column=0, padx=2, pady=5, sticky="e")

        # Entrada de texto para o nome do projeto (Create Project)
        self.entry_project_name = Entry(self.load_frame, width=30, font=("Calibri", 10))
        self.entry_project_name.grid(row=1, column=1, padx=2, pady=2, columnspan=2)

        # Botão para Load Image (Create Project)
        self.b_load_image = ttk.Button(self.load_frame, text="Load Image", style="TButton", command=self.load_image)
        self.b_load_image.grid(row=2, column=1, padx=2, pady=5)

        # Label informativa (Load Image / Create Project)
        self.msg_load = ttk.Label(self.load_frame, text="Load Image (.tiff) / Create Project", font=("Calibri", 12, "bold"))
        self.msg_load.grid(row=0, column=1, padx=5, pady=5)

        # Frame para Load Project
        self.load_project_frame = ttk.Frame(self.main_frame, relief="ridge")
        self.load_project_frame.grid(row=1, column=0, pady=10, sticky="nsew")

        # Botão para Load Project
        self.b_load_project = ttk.Button(self.load_project_frame, text="Load Project", style="TButton", command=self.load_project)
        self.b_load_project.grid(row=1, column=1, padx=5, pady=5)

        # Label informativa (Load Project)
        self.msg_load_project = ttk.Label(self.load_project_frame, text="Load Project", font=("Calibri", 12, "bold"))
        self.msg_load_project.grid(row=0, column=1, padx=5, pady=5)
        
        # Adicionar colunas vazias à esquerda e à direita do grid da grade inferior
        self.load_project_frame.grid_columnconfigure(0, weight=1)
        self.load_project_frame.grid_columnconfigure(2, weight=1)

        # Configurar pesos da grade para distribuir o espaço igualmente
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

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
