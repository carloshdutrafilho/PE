import string
from tkinter import Entry, Frame, Label, Button, messagebox, ttk, filedialog
from ttkthemes import ThemedStyle
import os

class LoadScreen(Frame):
    def __init__(self, master=None, app=None, image_viewer=None):
        super().__init__(master)
        self.app = app
        self.image_viewer = image_viewer
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
        self.b_load_image = ttk.Button(self.load_frame, text="Load Image", style="TButton", command=self.create_project)
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
        
        self.project_name = None
        self.selected_file = None
        
    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("TIFF files", "*.tiff;*.tif")])
        if file_path:
            self.image_viewer.load_image(self, file_path)
            self.update_recent_files(file_path)

    def create_project(self):
        if not self.validate_entry():
            # Se a validação falhar, exibe uma mensagem de aviso
            messagebox.showwarning("Warning", "Please enter a project name.")
            return

        # Verificar se self.app.selected_file não é None
        file_path = filedialog.askopenfilename(filetypes=[("TIFF files", "*.tiff;*.tif")])
        if file_path:
            self.selected_file = file_path
        
            image_directory = os.path.dirname(self.selected_file)
            image_name = self.selected_file

            # Obtenha o nome do projeto da entrada
            project_name = self.entry_project_name.get()

            # Criar a pasta do projeto se o nome do projeto for fornecido
            project_path = os.path.join(image_directory, project_name)
            os.makedirs(project_path, exist_ok=True)

            # Criar um arquivo de identificação dentro da pasta
            identification_file_path = os.path.join(project_path, "identification.txt")
            with open(identification_file_path, "w") as identification_file:
                identification_file.write(f"Project: {project_name}")
                identification_file.write(f"\nPath-{file_path}")

            print(f"Project folder created: {project_path}")

        # Usar o ImageViewer para carregar a imagem
        self.image_viewer.load_image(file_path)
        #self.master.destroy()

    def validate_entry(self):
        if not self.entry_project_name.get():
            print("Project name is required.")
            return False
        return True

    def load_project(self):
        # Implemente a lógica para carregar o projeto
        print("Loading project...")
