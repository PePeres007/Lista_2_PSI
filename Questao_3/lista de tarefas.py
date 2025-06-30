import tkinter as tk
from tkinter import messagebox

class TodoApp(tk.Tk):
    """
    Classe principal da aplicação de Lista de Tarefas com interface gráfica (GUI)
    usando a biblioteca Tkinter.
    """
    def __init__(self):
        super().__init__()

        # --- Configuração da Janela Principal ---
        self.title("Aplicativo de Lista de Tarefas")
        self.geometry("900x600")
        self.configure(bg="#f0f0f0")

        # --- Estrutura de Dados Principal ---
        self.listas_de_tarefas = {
            "a fazer": [],
            "executando": [],
            "pronta": []
        }
        self.LIMITE_EXECUTANDO = 10

        # --- Criação dos Elementos da Interface ---
        self.criar_widgets()
        self.atualizar_listboxes()

    def criar_widgets(self):
        """Cria e organiza todos os elementos visuais (widgets) na janela."""

        # --- Frame de Entrada (Topo) ---
        frame_entrada = tk.Frame(self, bg="#f0f0f0", padx=10, pady=10)
        frame_entrada.pack(fill=tk.X)

        label_nova_tarefa = tk.Label(frame_entrada, text="Nova Tarefa:", font=("Arial", 12), bg="#f0f0f0")
        label_nova_tarefa.pack(side=tk.LEFT, padx=5)

        self.entry_tarefa = tk.Entry(frame_entrada, font=("Arial", 12), width=50, relief=tk.SOLID, borderwidth=1)
        self.entry_tarefa.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        botao_adicionar = tk.Button(frame_entrada, text="Adicionar Tarefa", font=("Arial", 10, "bold"), 
                                    bg="#28a745", fg="white", command=self.adicionar_tarefa, relief=tk.FLAT, padx=10)
        botao_adicionar.pack(side=tk.LEFT, padx=5)

        # --- Frame Principal das Listas ---
        frame_listas = tk.Frame(self, bg="#f0f0f0", padx=10, pady=10)
        frame_listas.pack(fill=tk.BOTH, expand=True)
        frame_listas.grid_columnconfigure((0, 1, 2), weight=1) # Colunas com peso igual
        frame_listas.grid_rowconfigure(1, weight=1) # Linha da listbox com peso

        # --- Coluna "A Fazer" ---
        frame_a_fazer = tk.Frame(frame_listas, bg="#ffffff", padx=5, pady=5)
        frame_a_fazer.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=5)
        tk.Label(frame_a_fazer, text="A FAZER", font=("Arial", 14, "bold"), bg="#ffffff").pack(pady=5)
        self.listbox_a_fazer = tk.Listbox(frame_a_fazer, font=("Arial", 12), height=15, exportselection=False, relief=tk.FLAT)
        self.listbox_a_fazer.pack(fill=tk.BOTH, expand=True, pady=5)
        
        frame_botoes_a_fazer = tk.Frame(frame_a_fazer, bg="#ffffff")
        frame_botoes_a_fazer.pack(fill=tk.X, pady=5)
        tk.Button(frame_botoes_a_fazer, text="Mover para Executando →", bg="#007bff", fg="white", relief=tk.FLAT",
                  command=lambda: self.mover_tarefa("a fazer", "executando")).pack(side=tk.LEFT, expand=True)
        tk.Button(frame_botoes_a_fazer, text="Excluir", bg="#dc3545", fg="white", relief=tk.FLAT",
                  command=lambda: self.excluir_tarefa("a fazer")).pack(side=tk.RIGHT)

        # --- Coluna "Executando" ---
        frame_executando = tk.Frame(frame_listas, bg="#ffffff", padx=5, pady=5)
        frame_executando.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=5)
        tk.Label(frame_executando, text="EXECUTANDO", font=("Arial", 14, "bold"), bg="#ffffff").pack(pady=5)
        self.listbox_executando = tk.Listbox(frame_executando, font=("Arial", 12), height=15, exportselection=False, relief=tk.FLAT)
        self.listbox_executando.pack(fill=tk.BOTH, expand=True, pady=5)
        
        frame_botoes_executando = tk.Frame(frame_executando, bg="#ffffff")
        frame_botoes_executando.pack(fill=tk.X, pady=5)
        tk.Button(frame_botoes_executando, text="Mover para Pronta →", bg="#007bff", fg="white", relief=tk.FLAT",
                  command=lambda: self.mover_tarefa("executando", "pronta")).pack(side=tk.LEFT, expand=True)
        tk.Button(frame_botoes_executando, text="Excluir", bg="#dc3545", fg="white", relief=tk.FLAT",
                  command=lambda: self.excluir_tarefa("executando")).pack(side=tk.RIGHT)

        # --- Coluna "Pronta" ---
        frame_pronta = tk.Frame(frame_listas, bg="#ffffff", padx=5, pady=5)
        frame_pronta.grid(row=0, column=2, rowspan=2, sticky="nsew", padx=5)
        tk.Label(frame_pronta, text="PRONTA", font=("Arial", 14, "bold"), bg="#ffffff").pack(pady=5)
        self.listbox_pronta = tk.Listbox(frame_pronta, font=("Arial", 12), height=15, exportselection=False, relief=tk.FLAT)
        self.listbox_pronta.pack(fill=tk.BOTH, expand=True, pady=5)
        
        tk.Button(frame_pronta, text="Excluir", bg="#dc3545", fg="white", relief=tk.FLAT",
                  command=lambda: self.excluir_tarefa("pronta")).pack(fill=tk.X, pady=5)

    def adicionar_tarefa(self):
        """Lógica para adicionar uma nova tarefa."""
        nome_tarefa = self.entry_tarefa.get()

        if len(nome_tarefa) > 80:
            messagebox.showerror("Erro", "O nome da tarefa não pode ter mais de 80 caracteres.")
            return
        if not nome_tarefa.strip():
            messagebox.showerror("Erro", "O nome da tarefa não pode estar vazio.")
            return

        self.listas_de_tarefas["a fazer"].append(nome_tarefa)
        self.atualizar_listboxes()
        self.entry_tarefa.delete(0, tk.END) # Limpa o campo de entrada
        messagebox.showinfo("Sucesso", f"Tarefa '{nome_tarefa}' adicionada!")

    def mover_tarefa(self, de_status, para_status):
        """Lógica genérica para mover uma tarefa entre listas."""
        listbox_origem = getattr(self, f"listbox_{de_status.replace(' ', '_')}")
        
        try:
            # Pega o índice da tarefa selecionada na listbox de origem
            indices_selecionados = listbox_origem.curselection()
            if not indices_selecionados:
                messagebox.showwarning("Aviso", "Por favor, selecione uma tarefa para mover.")
                return
            
            indice_selecionado = indices_selecionados[0]
            tarefa_para_mover = listbox_origem.get(indice_selecionado)

            # Validação da regra de negócio para a lista "executando"
            if para_status == "executando" and len(self.listas_de_tarefas["executando"]) >= self.LIMITE_EXECUTANDO:
                messagebox.showerror("Erro de Limite", f"Limite de {self.LIMITE_EXECUTANDO} tarefas em execução atingido!")
                return

            # Atualiza a estrutura de dados
            self.listas_de_tarefas[de_status].remove(tarefa_para_mover)
            self.listas_de_tarefas[para_status].append(tarefa_para_mover)

            # Atualiza a interface
            self.atualizar_listboxes()

        except IndexError:
            messagebox.showwarning("Aviso", "Por favor, selecione uma tarefa para mover.")

    def excluir_tarefa(self, status):
        """Lógica para excluir uma tarefa da lista especificada."""
        listbox = getattr(self, f"listbox_{status.replace(' ', '_')}")
        
        try:
            indices_selecionados = listbox.curselection()
            if not indices_selecionados:
                messagebox.showwarning("Aviso", "Por favor, selecione uma tarefa para excluir.")
                return

            indice_selecionado = indices_selecionados[0]
            tarefa_para_excluir = listbox.get(indice_selecionado)
            
            # Confirmação antes de excluir
            if messagebox.askyesno("Confirmar Exclusão", f"Tem a certeza que deseja excluir a tarefa:\n'{tarefa_para_excluir}'?"):
                self.listas_de_tarefas[status].remove(tarefa_para_excluir)
                self.atualizar_listboxes()

        except IndexError:
            messagebox.showwarning("Aviso", "Por favor, selecione uma tarefa para excluir.")

    def atualizar_listboxes(self):
        """Limpa e re-popula todas as listboxes com os dados atuais."""
        self.listbox_a_fazer.delete(0, tk.END)
        self.listbox_executando.delete(0, tk.END)
        self.listbox_pronta.delete(0, tk.END)

        for tarefa in self.listas_de_tarefas["a fazer"]:
            self.listbox_a_fazer.insert(tk.END, tarefa)
        
        for tarefa in self.listas_de_tarefas["executando"]:
            self.listbox_executando.insert(tk.END, tarefa)

        for tarefa in self.listas_de_tarefas["pronta"]:
            self.listbox_pronta.insert(tk.END, tarefa)


if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()
