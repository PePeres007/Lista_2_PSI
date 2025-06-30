import tkinter as tk
from tkinter import messagebox, font
import json
import os

class TodoApp(tk.Tk):
    """
    Classe principal da aplicação de Lista de Tarefas com uma interface gráfica
    """
    def __init__(self):
        super().__init__()

        # --- Constantes e Nome do Ficheiro de Save ---
        self.ARQUIVO_SALVO = "tarefas.json"
        self.LIMITE_EXECUTANDO = 10

        # --- Estrutura de Dados ---
        # A estrutura é inicializada vazia e depois carregada do ficheiro.
        self.listas_de_tarefas = {
            "a fazer": [],
            "executando": [],
            "pronta": []
        }
        
        # --- Carregar Tarefas Guardadas ---
        self.carregar_tarefas()

        # --- Configuração de Cores e Fontes ---
        self.CORES = {
            "fundo": "#f7fafc", "coluna": "#e2e8f0", "cartao": "#ffffff",
            "texto": "#2d3748", "a fazer": "#9c0101", "executando": "#dd6b20",
            "pronta": "#38a169", "botao_add": "#48bb78", "botao_mover": "#4299e1",
            "botao_excluir": "#f56565"
        }
        self.FONTE_TITULO = font.Font(family="Helvetica", size=14, weight="bold")
        self.FONTE_TAREFA = font.Font(family="Helvetica", size=11)
        self.FONTE_BOTAO = font.Font(family="Helvetica", size=9, weight="bold")

        # --- Configuração da Janela Principal ---
        self.title("NextUp - Todo List App")
        self.geometry("1000x700")
        self.configure(bg=self.CORES["fundo"])

        # --- Criação dos Widgets e Atualização da UI ---
        self.criar_widgets_layout()
        self.atualizar_colunas_tarefas()

    def carregar_tarefas(self):
        """Verifica se existe um ficheiro de save e carrega as tarefas."""
        if os.path.exists(self.ARQUIVO_SALVO):
            try:
                with open(self.ARQUIVO_SALVO, 'r', encoding='utf-8') as f:
                    self.listas_de_tarefas = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                messagebox.showerror("Erro ao Carregar", f"Não foi possível carregar as tarefas: {e}")
                # Mantém as listas vazias se o ficheiro estiver corrompido

    def salvar_tarefas(self):
        """Guarda o estado atual das listas de tarefas no ficheiro JSON."""
        try:
            with open(self.ARQUIVO_SALVO, 'w', encoding='utf-8') as f:
                json.dump(self.listas_de_tarefas, f, ensure_ascii=False, indent=4)
        except IOError as e:
            messagebox.showerror("Erro ao Guardar", f"Não foi possível guardar as tarefas: {e}")

    def criar_widgets_layout(self):
        """Cria os frames principais e os elementos estáticos da interface."""
        frame_entrada = tk.Frame(self, bg=self.CORES["fundo"], padx=20, pady=15)
        frame_entrada.pack(fill=tk.X)

        label_nova_tarefa = tk.Label(frame_entrada, text="Nova Tarefa:", font=self.FONTE_TITULO, bg=self.CORES["fundo"], fg=self.CORES["texto"])
        label_nova_tarefa.pack(side=tk.LEFT, padx=(0, 10))

        self.entry_tarefa = tk.Entry(frame_entrada, font=self.FONTE_TAREFA, width=50, relief=tk.SOLID, borderwidth=1, bd=2, fg=self.CORES["texto"])
        self.entry_tarefa.pack(side=tk.LEFT, expand=True, fill=tk.X, ipady=5)

        botao_adicionar = tk.Button(frame_entrada, text="Adicionar", font=self.FONTE_BOTAO,
                                    bg=self.CORES["botao_add"], fg="white", command=self.adicionar_tarefa, relief=tk.FLAT, padx=15, pady=5)
        botao_adicionar.pack(side=tk.LEFT, padx=(10, 0))

        self.frame_kanban = tk.Frame(self, bg=self.CORES["fundo"], padx=10, pady=10)
        self.frame_kanban.pack(fill=tk.BOTH, expand=True)
        self.frame_kanban.grid_columnconfigure((0, 1, 2), weight=1, uniform="group1")
        self.frame_kanban.grid_rowconfigure(0, weight=1)

        self.colunas = {}
        for status in self.listas_de_tarefas.keys():
            col_idx = list(self.listas_de_tarefas.keys()).index(status)
            frame_coluna = tk.Frame(self.frame_kanban, bg=self.CORES["coluna"], padx=10, pady=10)
            frame_coluna.grid(row=0, column=col_idx, sticky="nsew", padx=10, pady=5)
            frame_header = tk.Frame(frame_coluna, bg=self.CORES["coluna"])
            frame_header.pack(fill=tk.X, pady=(0, 10))
            label_titulo = tk.Label(frame_header, text=status.upper(), font=self.FONTE_TITULO, 
                                    bg=self.CORES["coluna"], fg=self.CORES[status])
            label_titulo.pack(side=tk.LEFT)
            label_contador = tk.Label(frame_header, text="0", font=self.FONTE_BOTAO,
                                      bg=self.CORES[status], fg="white", padx=5)
            label_contador.pack(side=tk.RIGHT)
            frame_cartoes = tk.Frame(frame_coluna, bg=self.CORES["coluna"])
            frame_cartoes.pack(fill=tk.BOTH, expand=True)
            self.colunas[status] = {"frame": frame_cartoes, "contador": label_contador}

    def atualizar_colunas_tarefas(self):
        """Limpa e redesenha todos os cartões de tarefas em todas as colunas."""
        for status, data in self.colunas.items():
            for widget in data["frame"].winfo_children():
                widget.destroy()
            num_tarefas = len(self.listas_de_tarefas[status])
            data["contador"].config(text=str(num_tarefas))
            for tarefa in self.listas_de_tarefas[status]:
                self.criar_cartao_tarefa(data["frame"], tarefa, status)

    def criar_cartao_tarefa(self, parent_frame, nome_tarefa, status):
        """Cria um widget de 'cartão' para uma única tarefa."""
        cartao = tk.Frame(parent_frame, bg=self.CORES["cartao"], padx=10, pady=10, relief=tk.SOLID, bd=1, borderwidth=1)
        cartao.pack(fill=tk.X, pady=5)
        label_tarefa = tk.Label(cartao, text=nome_tarefa, font=self.FONTE_TAREFA, bg=self.CORES["cartao"],
                                fg=self.CORES["texto"], wraplength=220, justify=tk.LEFT)
        label_tarefa.pack(fill=tk.X, pady=(0, 10))
        frame_botoes = tk.Frame(cartao, bg=self.CORES["cartao"])
        frame_botoes.pack(fill=tk.X)
        tk.Button(frame_botoes, text="Excluir", font=self.FONTE_BOTAO, bg=self.CORES["botao_excluir"], fg="white", relief=tk.FLAT,
                  command=lambda t=nome_tarefa, s=status: self.excluir_tarefa(t, s)).pack(side=tk.RIGHT)
        if status == "a fazer":
            tk.Button(frame_botoes, text="Mover →", font=self.FONTE_BOTAO, bg=self.CORES["botao_mover"], fg="white", relief=tk.FLAT,
                      command=lambda t=nome_tarefa: self.mover_tarefa(t, "a fazer", "executando")).pack(side=tk.RIGHT, padx=(0, 5))
        elif status == "executando":
            tk.Button(frame_botoes, text="Mover →", font=self.FONTE_BOTAO, bg=self.CORES["botao_mover"], fg="white", relief=tk.FLAT,
                      command=lambda t=nome_tarefa: self.mover_tarefa(t, "executando", "pronta")).pack(side=tk.RIGHT, padx=(0, 5))

    def adicionar_tarefa(self):
        """Lógica para adicionar uma nova tarefa."""
        nome_tarefa = self.entry_tarefa.get().strip()
        if not nome_tarefa:
            messagebox.showwarning("Aviso", "O nome da tarefa não pode estar vazio.")
            return
        if len(nome_tarefa) > 80:
            messagebox.showwarning("Aviso", "O nome da tarefa excede 80 caracteres.")
            return
        self.listas_de_tarefas["a fazer"].append(nome_tarefa)
        self.atualizar_colunas_tarefas()
        self.salvar_tarefas()
        self.entry_tarefa.delete(0, tk.END)

    def mover_tarefa(self, tarefa, de_status, para_status):
        """Lógica para mover uma tarefa entre colunas."""
        if para_status == "executando" and len(self.listas_de_tarefas["executando"]) >= self.LIMITE_EXECUTANDO:
            messagebox.showerror("Erro de Limite", f"Limite de {self.LIMITE_EXECUTANDO} tarefas em execução atingido!")
            return
        self.listas_de_tarefas[de_status].remove(tarefa)
        self.listas_de_tarefas[para_status].append(tarefa)
        self.atualizar_colunas_tarefas()
        self.salvar_tarefas()

    def excluir_tarefa(self, tarefa, status):
        """Lógica para excluir uma tarefa."""
        if messagebox.askyesno("Confirmar Exclusão", f"Tem a certeza que deseja excluir a tarefa:\n'{tarefa}'?"):
            self.listas_de_tarefas[status].remove(tarefa)
            self.atualizar_colunas_tarefas()
            self.salvar_tarefas()

if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()
