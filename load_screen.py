import string
from tkinter import Entry, Frame, Label, Button, Toplevel, messagebox, ttk, filedialog
from tkinter.simpledialog import askstring
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

        self.project_path = None

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
            messagebox.showwarning("Warning", "Please enter a project name.")
            return

        file_path = filedialog.askopenfilename(filetypes=[("TIFF files", "*.tiff;*.tif")])

        if file_path:
            if not file_path.lower().endswith(('.tiff', '.tif')):
                messagebox.showwarning("Warning", "Please select a TIFF file.")
                return

            self.selected_file = file_path
    
            image_directory = os.path.dirname(self.selected_file)
            image_name = self.selected_file

            self.project_name = self.entry_project_name.get()

            default_directory = "C:/MedicAnalysis/Projects"
            if not os.path.exists(default_directory):
                os.makedirs(default_directory)
        
            self.project_path = os.path.join(default_directory, self.project_name)

            while os.path.exists(self.project_path):
                if not self.project_name:
                    new_project_name = askstring("Invalid Project Name", f"The project needs a name. Please enter a new name: ")
                else:
                    new_project_name = askstring("Invalid Project Name", f"A project with the name '{self.project_name}' already exists. Please enter a new name:")
                self.project_name = new_project_name
                self.project_path = os.path.join(default_directory, self.project_name)

            os.makedirs(self.project_path)

            self.identification_file_path = os.path.join(self.project_path, "identification.txt")
            with open(self.identification_file_path, "w") as identification_file:
                identification_file.write(f"Project: {self.project_name}")
                identification_file.write(f"\nPath-{file_path}")

            print(f"Project folder created: {self.project_path}")
            self.master.withdraw()
            self.app.enable_functionalities_post_load()
            self.image_viewer.load_image(file_path)

    def validate_entry(self):
        if not self.entry_project_name.get():
            print("Project name is required.")
            return False
        return True

    def load_project(self):
        selected_directory = filedialog.askdirectory()

        if selected_directory:
            identification_file_path = os.path.join(selected_directory, "identification.txt")

            if os.path.exists(identification_file_path):
                with open(identification_file_path, "r") as identification_file:
                    if (identification_file.readline().strip() == ""): 
                        project_name_line = identification_file.readline().strip()
                        path_line = identification_file.readline().strip()

                    if not project_name_line.startswith("Project:"):
                        messagebox.showwarning("Warning", "Invalid format in identification file.")
                        return

                    self.project_name = project_name_line.split(":", 1)[1].strip()

                    if not path_line.startswith("Path-"):
                        messagebox.showwarning("Warning", "Invalid format in identification file.")
                        return

                    image_path = path_line.split("-", 1)[1].strip()

                print(f"Loaded project: {self.project_name}")
                self.project_path = selected_directory
                self.selected_file = image_path
                print(f"Image path: {image_path}")

                self.master.withdraw()
                self.app.enable_functionalities_post_load()
                #self.app.charge_data_from_csv()
                self.image_viewer.load_image(image_path)

                csv_path = os.path.join(selected_directory, "data_viewer_setup.csv")
                if os.path.exists(csv_path):
                    self.app.data_viewer.load_csv(csv_path)
            else:
                messagebox.showwarning("Warning", "Selected folder does not contain a valid identification file.")
        else:
            messagebox.showwarning("Warning", "No folder selected.")

    def get_project_path(self):
        return self.project_path
    
    def get_image_path(self):
        return self.selected_file