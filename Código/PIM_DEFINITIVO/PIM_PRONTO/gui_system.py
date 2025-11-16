"""
Sistema Acadêmico - Interface Gráfica com Tkinter
Parte 1: Estrutura Base e Tela de Login
"""

import tkinter as tk
from tkinter import ttk, messagebox
import database as db
from models import Aluno, Turma, Aula, Atividade, Nota, Chamada, Professor
from datetime import datetime

class AcademicSystemGUI:
    """Classe principal da interface gráfica do sistema acadêmico"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Acadêmico PIM")
        self.root.geometry("900x600")
        self.root.resizable(False, False)
        
        # Variáveis de sessão do usuário
        self.usuario_id = None
        self.usuario_nome = None
        self.usuario_papel = None
        
        # Cores do tema
        self.colors = {
            'primary': '#2C3E50',
            'secondary': '#34495E',
            'accent': '#3498DB',
            'success': '#27AE60',
            'warning': '#F39C12',
            'danger': '#E74C3C',
            'light': '#ECF0F1',
            'white': '#FFFFFF'
        }
        
        # Configura o estilo
        self.setup_styles()
        
        # Inicializa os arquivos do banco de dados
        db.inicializar_arquivos()
        
        # Mostra a tela de login
        self.mostrar_tela_login()
    
    def setup_styles(self):
        """Configura os estilos visuais da interface"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Estilo para botões
        style.configure('Primary.TButton',
                       background=self.colors['accent'],
                       foreground=self.colors['white'],
                       borderwidth=0,
                       focuscolor='none',
                       font=('Segoe UI', 10))
        
        style.map('Primary.TButton',
                 background=[('active', '#2980B9')])
        
        # Estilo para labels de título
        style.configure('Title.TLabel',
                       font=('Segoe UI', 18, 'bold'),
                       foreground=self.colors['primary'])
        
        # Estilo para labels normais
        style.configure('Normal.TLabel',
                       font=('Segoe UI', 10),
                       foreground=self.colors['secondary'])
    
    def limpar_janela(self):
        """Remove todos os widgets da janela"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def mostrar_tela_login(self):
        """Exibe a tela de login do sistema"""
        self.limpar_janela()
        
        # Frame principal com cor de fundo
        main_frame = tk.Frame(self.root, bg=self.colors['light'])
        main_frame.pack(fill='both', expand=True)
        
        # Frame central para o formulário de login
        login_frame = tk.Frame(main_frame, bg=self.colors['white'], 
                              relief='raised', borderwidth=2)
        login_frame.place(relx=0.5, rely=0.5, anchor='center', 
                         width=400, height=350)
        
        # Título
        title_label = tk.Label(login_frame, 
                              text="Sistema Acadêmico PIM",
                              font=('Segoe UI', 20, 'bold'),
                              bg=self.colors['white'],
                              fg=self.colors['primary'])
        title_label.pack(pady=(30, 10))
        
        subtitle_label = tk.Label(login_frame,
                                 text="Faça login para continuar",
                                 font=('Segoe UI', 10),
                                 bg=self.colors['white'],
                                 fg=self.colors['secondary'])
        subtitle_label.pack(pady=(0, 30))
        
        # Campo de usuário
        user_label = tk.Label(login_frame,
                             text="Usuário:",
                             font=('Segoe UI', 10),
                             bg=self.colors['white'],
                             fg=self.colors['secondary'])
        user_label.pack(pady=(0, 5))
        
        self.username_entry = tk.Entry(login_frame,
                                       font=('Segoe UI', 11),
                                       relief='solid',
                                       borderwidth=1)
        self.username_entry.pack(pady=(0, 15), padx=40, fill='x')
        self.username_entry.focus()
        
        # Campo de senha
        pass_label = tk.Label(login_frame,
                             text="Senha:",
                             font=('Segoe UI', 10),
                             bg=self.colors['white'],
                             fg=self.colors['secondary'])
        pass_label.pack(pady=(0, 5))
        
        self.password_entry = tk.Entry(login_frame,
                                       font=('Segoe UI', 11),
                                       show='●',
                                       relief='solid',
                                       borderwidth=1)
        self.password_entry.pack(pady=(0, 25), padx=40, fill='x')
        
        # Bind Enter para fazer login
        self.password_entry.bind('<Return>', lambda e: self.fazer_login())
        self.username_entry.bind('<Return>', lambda e: self.password_entry.focus())
        
        # Botão de login
        login_button = tk.Button(login_frame,
                                text="ENTRAR",
                                font=('Segoe UI', 11, 'bold'),
                                bg=self.colors['accent'],
                                fg=self.colors['white'],
                                relief='flat',
                                cursor='hand2',
                                command=self.fazer_login)
        login_button.pack(pady=(0, 20), padx=40, fill='x', ipady=8)
        
        # Rodapé
        footer_label = tk.Label(main_frame,
                               text="© 2025 Sistema Acadêmico PIM",
                               font=('Segoe UI', 8),
                               bg=self.colors['light'],
                               fg=self.colors['secondary'])
        footer_label.pack(side='bottom', pady=10)
    
    def fazer_login(self):
        """Processa o login do usuário"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showwarning("Campos vazios", 
                                 "Por favor, preencha todos os campos.")
            return
        
        # Verifica as credenciais
        id_usuario, papel, nome = db.verificar_usuario(username, password)
        
        if papel:
            self.usuario_id = id_usuario
            self.usuario_nome = nome
            self.usuario_papel = papel
            
            messagebox.showinfo("Login bem-sucedido", 
                              f"Bem-vindo(a), {nome}!")
            
            # Redireciona para o menu apropriado
            if papel == 'adm':
                self.mostrar_menu_administrador()
            elif papel == 'professor':
                self.mostrar_menu_professor()
            elif papel == 'aluno':
                self.mostrar_menu_aluno()
        else:
            messagebox.showerror("Erro de Login",
                               "Usuário ou senha inválidos, ou usuário inativo.")
            self.password_entry.delete(0, 'end')
    
    def criar_header(self, parent):
        """Cria o cabeçalho com informações do usuário e botão de logout"""
        header = tk.Frame(parent, bg=self.colors['primary'], height=60)
        header.pack(fill='x', side='top')
        header.pack_propagate(False)
        
        # Informações do usuário
        user_info = tk.Label(header,
                            text=f"{self.usuario_nome} ({self.usuario_papel.upper()})",
                            font=('Segoe UI', 11, 'bold'),
                            bg=self.colors['primary'],
                            fg=self.colors['white'])
        user_info.pack(side='left', padx=20)
        
        # Botão de logout
        logout_btn = tk.Button(header,
                              text="Sair",
                              font=('Segoe UI', 10),
                              bg=self.colors['danger'],
                              fg=self.colors['white'],
                              relief='flat',
                              cursor='hand2',
                              command=self.fazer_logout)
        logout_btn.pack(side='right', padx=20, ipadx=15, ipady=5)
        
        return header
    
    def fazer_logout(self):
        """Realiza o logout e retorna à tela de login"""
        if messagebox.askyesno("Confirmar Logout", 
                              "Deseja realmente sair do sistema?"):
            self.usuario_id = None
            self.usuario_nome = None
            self.usuario_papel = None
            self.mostrar_tela_login()
    
    def mostrar_menu_administrador(self):
        """Exibe o menu principal do administrador com abas"""
        self.limpar_janela()
        self.criar_header(self.root)
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg=self.colors['light'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Notebook (Abas)
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill='both', expand=True)
        
        # Aba 1: Usuários
        tab_usuarios = tk.Frame(notebook, bg=self.colors['white'])
        notebook.add(tab_usuarios, text='Usuários')
        self.criar_aba_usuarios_adm(tab_usuarios)
        
        # Aba 2: Turmas
        tab_turmas = tk.Frame(notebook, bg=self.colors['white'])
        notebook.add(tab_turmas, text='Turmas')
        self.criar_aba_turmas_adm(tab_turmas)
        
        # Aba 3: Aulas
        tab_aulas = tk.Frame(notebook, bg=self.colors['white'])
        notebook.add(tab_aulas, text='Aulas')
        self.criar_aba_aulas_adm(tab_aulas)
        
        # Aba 4: Atividades e Notas
        tab_atividades = tk.Frame(notebook, bg=self.colors['white'])
        notebook.add(tab_atividades, text='Atividades e Notas')
        self.criar_aba_atividades_adm(tab_atividades)
        
        # Aba 5: Chamadas
        tab_chamadas = tk.Frame(notebook, bg=self.colors['white'])
        notebook.add(tab_chamadas, text='Chamadas')
        self.criar_aba_chamadas_adm(tab_chamadas)
    
    def criar_aba_usuarios_adm(self, parent):
        """Cria a aba de gerenciamento de usuários para o administrador"""
        # Frame de botões
        btn_frame = tk.Frame(parent, bg=self.colors['white'])
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(btn_frame, text="Cadastrar Administrador", 
                 bg=self.colors['accent'], fg=self.colors['white'],
                 font=('Segoe UI', 10), relief='flat', cursor='hand2',
                 command=self.cadastrar_administrador).pack(side='left', padx=5, ipady=5, ipadx=10)
        
        tk.Button(btn_frame, text="Cadastrar Professor",
                 bg=self.colors['accent'], fg=self.colors['white'],
                 font=('Segoe UI', 10), relief='flat', cursor='hand2',
                 command=self.cadastrar_professor).pack(side='left', padx=5, ipady=5, ipadx=10)
        
        tk.Button(btn_frame, text="Cadastrar Aluno",
                 bg=self.colors['accent'], fg=self.colors['white'],
                 font=('Segoe UI', 10), relief='flat', cursor='hand2',
                 command=self.cadastrar_aluno).pack(side='left', padx=5, ipady=5, ipadx=10)
        
        tk.Button(btn_frame, text="Ativar/Desativar Usuário",
                 bg=self.colors['warning'], fg=self.colors['white'],
                 font=('Segoe UI', 10), relief='flat', cursor='hand2',
                 command=self.ativar_desativar_usuario).pack(side='left', padx=5, ipady=5, ipadx=10)
        
        tk.Button(btn_frame, text="Atualizar Lista",
                 bg=self.colors['success'], fg=self.colors['white'],
                 font=('Segoe UI', 10), relief='flat', cursor='hand2',
                 command=lambda: self.listar_usuarios_table()).pack(side='right', padx=5, ipady=5, ipadx=10)
        
        # Frame para a tabela
        table_frame = tk.Frame(parent, bg=self.colors['white'])
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(table_frame)
        scrollbar.pack(side='right', fill='y')
        
        # Treeview para listar usuários
        self.usuarios_tree = ttk.Treeview(table_frame, 
                                         columns=('ID', 'Nome', 'Usuário', 'Papel', 'RA', 'Ativo'),
                                         show='headings',
                                         yscrollcommand=scrollbar.set)
        
        # Configurar colunas
        self.usuarios_tree.heading('ID', text='ID')
        self.usuarios_tree.heading('Nome', text='Nome')
        self.usuarios_tree.heading('Usuário', text='Usuário')
        self.usuarios_tree.heading('Papel', text='Papel')
        self.usuarios_tree.heading('RA', text='RA')
        self.usuarios_tree.heading('Ativo', text='Ativo')
        
        self.usuarios_tree.column('ID', width=50)
        self.usuarios_tree.column('Nome', width=200)
        self.usuarios_tree.column('Usuário', width=150)
        self.usuarios_tree.column('Papel', width=100)
        self.usuarios_tree.column('RA', width=100)
        self.usuarios_tree.column('Ativo', width=80)
        
        scrollbar.config(command=self.usuarios_tree.yview)
        self.usuarios_tree.pack(fill='both', expand=True)
        
        # Carregar dados
        self.listar_usuarios_table()
    
    def listar_usuarios_table(self):
        """Carrega os usuários na tabela"""
        # Limpar tabela
        for item in self.usuarios_tree.get_children():
            self.usuarios_tree.delete(item)
        
        # Carregar usuários
        usuarios = db.listar_usuarios()
        for usuario in usuarios:
            id_u, username, _, papel, nome, ra, ativo = usuario
            ra_str = ra if ra else "N/A"
            ativo_str = "Sim" if ativo == '1' else "Não"
            self.usuarios_tree.insert('', 'end', values=(id_u, nome, username, papel, ra_str, ativo_str))
    
    def cadastrar_administrador(self):
        """Janela para cadastrar um novo administrador"""
        self.janela_cadastro_usuario('adm', 'Administrador')
    
    def cadastrar_professor(self):
        """Janela para cadastrar um novo professor"""
        self.janela_cadastro_usuario('professor', 'Professor')
    
    def cadastrar_aluno(self):
        """Janela para cadastrar um novo aluno"""
        self.janela_cadastro_usuario('aluno', 'Aluno')
    
    def janela_cadastro_usuario(self, papel, titulo):
        """Janela genérica para cadastro de usuário"""
        janela = tk.Toplevel(self.root)
        janela.title(f"Cadastrar {titulo}")
        janela.geometry("400x350")
        janela.resizable(False, False)
        janela.grab_set()
        
        frame = tk.Frame(janela, bg=self.colors['white'])
        frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Nome completo
        tk.Label(frame, text="Nome Completo:", bg=self.colors['white'],
                font=('Segoe UI', 10)).grid(row=0, column=0, sticky='w', pady=5)
        nome_entry = tk.Entry(frame, font=('Segoe UI', 10), width=30)
        nome_entry.grid(row=0, column=1, pady=5)
        nome_entry.focus()
        
        # Usuário (login)
        tk.Label(frame, text="Usuário (login):", bg=self.colors['white'],
                font=('Segoe UI', 10)).grid(row=1, column=0, sticky='w', pady=5)
        user_entry = tk.Entry(frame, font=('Segoe UI', 10), width=30)
        user_entry.grid(row=1, column=1, pady=5)
        
        # Senha
        tk.Label(frame, text="Senha:", bg=self.colors['white'],
                font=('Segoe UI', 10)).grid(row=2, column=0, sticky='w', pady=5)
        pass_entry = tk.Entry(frame, font=('Segoe UI', 10), show='●', width=30)
        pass_entry.grid(row=2, column=1, pady=5)
        
        # Campo extra para aluno (turma)
        turma_combo = None
        if papel == 'aluno':
            tk.Label(frame, text="Turma (opcional):", bg=self.colors['white'],
                    font=('Segoe UI', 10)).grid(row=3, column=0, sticky='w', pady=5)
            turmas = db.listar_turmas()
            turmas_nomes = ["Nenhuma"] + [t.nome_disciplina for t in turmas]
            turma_combo = ttk.Combobox(frame, values=turmas_nomes, 
                                      font=('Segoe UI', 10), width=28, state='readonly')
            turma_combo.set("Nenhuma")
            turma_combo.grid(row=3, column=1, pady=5)
        
        def salvar():
            nome = nome_entry.get().strip()
            username = user_entry.get().strip()
            senha = pass_entry.get()
            
            if not nome or not username or not senha:
                messagebox.showwarning("Campos vazios", "Preencha todos os campos!", parent=janela)
                return
            
            if db.usuario_existe(username):
                messagebox.showerror("Erro", "Nome de usuário já existe!", parent=janela)
                return
            
            id_usuario = db.get_proximo_id(db.ARQUIVO_USUARIOS)
            
            if papel == 'aluno':
                ra = db.gerar_novo_ra('aluno')
                
                # Verifica se uma turma foi selecionada
                id_turma = None
                turma_selecionada = turma_combo.get()
                if turma_selecionada != "Nenhuma":
                    turmas = db.listar_turmas()
                    turma_obj = next((t for t in turmas if t.nome_disciplina == turma_selecionada), None)
                    if turma_obj:
                        id_turma = turma_obj.id
                
                aluno = Aluno(id=id_usuario, nome=nome, ra=ra, id_turma=id_turma)
                db.salvar_aluno(aluno)
                db.salvar_usuario(id=id_usuario, username=username, senha=senha, 
                                papel='aluno', nome=nome, ra=ra, ativo=True)
                
                if id_turma:
                    db.adicionar_aluno_a_turma(id_usuario, id_turma)
                
            elif papel == 'professor':
                ra = db.gerar_novo_ra('professor')
                professor = Professor(id=id_usuario, nome=nome, ra=ra)
                db.salvar_professor(professor)
                db.salvar_usuario(id=id_usuario, username=username, senha=senha,
                                papel='professor', nome=nome, ra=ra, ativo=True)
            else:  # adm
                db.salvar_usuario(id=id_usuario, username=username, senha=senha,
                                papel='adm', nome=nome, ra=None, ativo=True)
            
            messagebox.showinfo("Sucesso", f"{titulo} cadastrado com sucesso!", parent=janela)
            janela.destroy()
            self.listar_usuarios_table()
        
        # Botão salvar
        tk.Button(frame, text="Salvar", bg=self.colors['success'], fg=self.colors['white'],
                 font=('Segoe UI', 10, 'bold'), relief='flat', cursor='hand2',
                 command=salvar).grid(row=4, column=0, columnspan=2, pady=20, ipadx=30, ipady=5)
    
    def ativar_desativar_usuario(self):
        """Ativa ou desativa um usuário selecionado"""
        selecionado = self.usuarios_tree.selection()
        if not selecionado:
            messagebox.showwarning("Nenhuma seleção", "Selecione um usuário na lista.")
            return
        
        item = self.usuarios_tree.item(selecionado[0])
        valores = item['values']
        id_usuario = valores[0]
        nome = valores[1]
        ativo_atual = valores[5] == "Sim"
        
        acao = "desativar" if ativo_atual else "ativar"
        if messagebox.askyesno("Confirmar", f"Deseja {acao} o usuário '{nome}'?"):
            db.set_usuario_ativo(str(id_usuario), not ativo_atual)
            messagebox.showinfo("Sucesso", f"Usuário '{nome}' foi {acao}do!")
            self.listar_usuarios_table()
    
    def criar_aba_turmas_adm(self, parent):
        """Cria a aba de gerenciamento de turmas"""
        # Frame de botões
        btn_frame = tk.Frame(parent, bg=self.colors['white'])
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(btn_frame, text="Cadastrar Turma",
                 bg=self.colors['accent'], fg=self.colors['white'],
                 font=('Segoe UI', 10), relief='flat', cursor='hand2',
                 command=self.cadastrar_turma).pack(side='left', padx=5, ipady=5, ipadx=10)
        
        tk.Button(btn_frame, text="Adicionar Aluno à Turma",
                 bg=self.colors['accent'], fg=self.colors['white'],
                 font=('Segoe UI', 10), relief='flat', cursor='hand2',
                 command=self.adicionar_aluno_turma).pack(side='left', padx=5, ipady=5, ipadx=10)
        
        tk.Button(btn_frame, text="Atualizar Lista",
                 bg=self.colors['success'], fg=self.colors['white'],
                 font=('Segoe UI', 10), relief='flat', cursor='hand2',
                 command=lambda: self.listar_turmas_table()).pack(side='right', padx=5, ipady=5, ipadx=10)
        
        # Frame para a tabela
        table_frame = tk.Frame(parent, bg=self.colors['white'])
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(table_frame)
        scrollbar.pack(side='right', fill='y')
        
        # Treeview
        self.turmas_tree = ttk.Treeview(table_frame,
                                       columns=('ID', 'Nome', 'Qtd Alunos', 'Alunos'),
                                       show='headings',
                                       yscrollcommand=scrollbar.set)
        
        self.turmas_tree.heading('ID', text='ID')
        self.turmas_tree.heading('Nome', text='Nome da Turma')
        self.turmas_tree.heading('Qtd Alunos', text='Qtd Alunos')
        self.turmas_tree.heading('Alunos', text='Alunos')
        
        self.turmas_tree.column('ID', width=50)
        self.turmas_tree.column('Nome', width=150)
        self.turmas_tree.column('Qtd Alunos', width=100)
        self.turmas_tree.column('Alunos', width=400)
        
        scrollbar.config(command=self.turmas_tree.yview)
        self.turmas_tree.pack(fill='both', expand=True)
        
        self.listar_turmas_table()
    
    def listar_turmas_table(self):
        """Carrega turmas na tabela"""
        for item in self.turmas_tree.get_children():
            self.turmas_tree.delete(item)
        
        turmas = db.listar_turmas()
        todos_alunos = {al.id: al for al in db.listar_alunos(filter_ativos=False)}
        
        for turma in turmas:
            qtd = len(turma.id_alunos)
            alunos_nomes = []
            for id_aluno in turma.id_alunos:
                if id_aluno in todos_alunos:
                    alunos_nomes.append(todos_alunos[id_aluno].nome)
            
            alunos_str = ", ".join(alunos_nomes) if alunos_nomes else "Nenhum aluno"
            self.turmas_tree.insert('', 'end', values=(turma.id, turma.nome_disciplina, qtd, alunos_str))
    
    def cadastrar_turma(self):
        """Janela para cadastrar nova turma"""
        janela = tk.Toplevel(self.root)
        janela.title("Cadastrar Nova Turma")
        janela.geometry("500x400")
        janela.resizable(False, False)
        janela.grab_set()
        
        frame = tk.Frame(janela, bg=self.colors['white'])
        frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(frame, text="Nome da Turma:", bg=self.colors['white'],
                font=('Segoe UI', 10)).pack(pady=5)
        nome_entry = tk.Entry(frame, font=('Segoe UI', 10), width=40)
        nome_entry.pack(pady=5)
        nome_entry.focus()
        
        tk.Label(frame, text="Alunos disponíveis (sem turma):", bg=self.colors['white'],
                font=('Segoe UI', 10)).pack(pady=10)
        
        # Listbox para selecionar alunos
        list_frame = tk.Frame(frame, bg=self.colors['white'])
        list_frame.pack(fill='both', expand=True, pady=5)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        alunos_listbox = tk.Listbox(list_frame, selectmode='multiple',
                                    font=('Segoe UI', 9),
                                    yscrollcommand=scrollbar.set)
        alunos_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=alunos_listbox.yview)
        
        # Carregar alunos sem turma
        alunos_disponiveis = db.listar_alunos_sem_turma()
        for aluno in alunos_disponiveis:
            alunos_listbox.insert('end', f"{aluno.id} - {aluno.nome} (RA: {aluno.ra})")
        
        def salvar():
            nome_turma = nome_entry.get().strip()
            if not nome_turma:
                messagebox.showwarning("Campo vazio", "Digite o nome da turma!", parent=janela)
                return
            
            # Pegar IDs dos alunos selecionados
            indices_selecionados = alunos_listbox.curselection()
            ids_alunos = []
            for idx in indices_selecionados:
                texto = alunos_listbox.get(idx)
                id_aluno = texto.split(' - ')[0]
                ids_alunos.append(id_aluno)
            
            # Criar turma
            novo_id = str(db.get_proximo_id(db.ARQUIVO_TURMAS))
            turma = Turma(id=novo_id, nome_disciplina=nome_turma, id_alunos=ids_alunos)
            db.salvar_turma(turma)
            
            # Atualizar alunos
            if ids_alunos:
                db.atualizar_turma_alunos(ids_alunos, novo_id)
            
            messagebox.showinfo("Sucesso", f"Turma '{nome_turma}' cadastrada com {len(ids_alunos)} aluno(s)!", parent=janela)
            janela.destroy()
            self.listar_turmas_table()
        
        tk.Button(frame, text="Salvar Turma", bg=self.colors['success'],
                 fg=self.colors['white'], font=('Segoe UI', 10, 'bold'),
                 relief='flat', cursor='hand2',
                 command=salvar).pack(pady=15, ipadx=20, ipady=5)
    
    def adicionar_aluno_turma(self):
        """Adiciona um aluno existente a uma turma"""
        janela = tk.Toplevel(self.root)
        janela.title("Adicionar Aluno à Turma")
        janela.geometry("400x250")
        janela.resizable(False, False)
        janela.grab_set()
        
        frame = tk.Frame(janela, bg=self.colors['white'])
        frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Selecionar aluno
        tk.Label(frame, text="Selecione o Aluno:", bg=self.colors['white'],
                font=('Segoe UI', 10)).pack(pady=5)
        
        alunos_disponiveis = db.listar_alunos_sem_turma()
        if not alunos_disponiveis:
            tk.Label(frame, text="Nenhum aluno disponível sem turma.",
                    bg=self.colors['white'], fg=self.colors['danger'],
                    font=('Segoe UI', 10)).pack(pady=20)
            return
        
        alunos_opcoes = [f"{a.id} - {a.nome} (RA: {a.ra})" for a in alunos_disponiveis]
        aluno_combo = ttk.Combobox(frame, values=alunos_opcoes,
                                  font=('Segoe UI', 9), width=35, state='readonly')
        aluno_combo.pack(pady=5)
        
        # Selecionar turma
        tk.Label(frame, text="Selecione a Turma:", bg=self.colors['white'],
                font=('Segoe UI', 10)).pack(pady=5)
        
        turmas = db.listar_turmas()
        if not turmas:
            tk.Label(frame, text="Nenhuma turma cadastrada.",
                    bg=self.colors['white'], fg=self.colors['danger'],
                    font=('Segoe UI', 10)).pack(pady=20)
            return
        
        turmas_opcoes = [f"{t.id} - {t.nome_disciplina}" for t in turmas]
        turma_combo = ttk.Combobox(frame, values=turmas_opcoes,
                                  font=('Segoe UI', 9), width=35, state='readonly')
        turma_combo.pack(pady=5)
        
        def adicionar():
            if not aluno_combo.get() or not turma_combo.get():
                messagebox.showwarning("Seleção incompleta", "Selecione aluno e turma!", parent=janela)
                return
            
            id_aluno = aluno_combo.get().split(' - ')[0]
            id_turma = turma_combo.get().split(' - ')[0]
            
            db.atualizar_turma_aluno(id_aluno, id_turma)
            db.adicionar_aluno_a_turma(id_aluno, id_turma)
            
            messagebox.showinfo("Sucesso", "Aluno adicionado à turma com sucesso!", parent=janela)
            janela.destroy()
            self.listar_turmas_table()
        
        tk.Button(frame, text="Adicionar", bg=self.colors['success'],
                 fg=self.colors['white'], font=('Segoe UI', 10, 'bold'),
                 relief='flat', cursor='hand2',
                 command=adicionar).pack(pady=15, ipadx=30, ipady=5)
    
    def criar_aba_aulas_adm(self, parent):
        """Cria a aba de gerenciamento de aulas"""
        # Frame de botões
        btn_frame = tk.Frame(parent, bg=self.colors['white'])
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(btn_frame, text="Registrar Aula",
                 bg=self.colors['accent'], fg=self.colors['white'],
                 font=('Segoe UI', 10), relief='flat', cursor='hand2',
                 command=self.registrar_aula_adm).pack(side='left', padx=5, ipady=5, ipadx=10)
        
        tk.Button(btn_frame, text="Atualizar Lista",
                 bg=self.colors['success'], fg=self.colors['white'],
                 font=('Segoe UI', 10), relief='flat', cursor='hand2',
                 command=lambda: self.listar_aulas_table()).pack(side='right', padx=5, ipady=5, ipadx=10)
        
        # Tabela de aulas
        table_frame = tk.Frame(parent, bg=self.colors['white'])
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(table_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.aulas_tree = ttk.Treeview(table_frame,
                                      columns=('ID', 'Turma', 'Data', 'Tópico', 'Professor'),
                                      show='headings',
                                      yscrollcommand=scrollbar.set)
        
        self.aulas_tree.heading('ID', text='ID')
        self.aulas_tree.heading('Turma', text='Turma')
        self.aulas_tree.heading('Data', text='Data')
        self.aulas_tree.heading('Tópico', text='Tópico')
        self.aulas_tree.heading('Professor', text='Professor')
        
        self.aulas_tree.column('ID', width=50)
        self.aulas_tree.column('Turma', width=150)
        self.aulas_tree.column('Data', width=100)
        self.aulas_tree.column('Tópico', width=250)
        self.aulas_tree.column('Professor', width=150)
        
        scrollbar.config(command=self.aulas_tree.yview)
        self.aulas_tree.pack(fill='both', expand=True)
        
        self.listar_aulas_table()
    
    def listar_aulas_table(self):
        """Carrega aulas na tabela"""
        for item in self.aulas_tree.get_children():
            self.aulas_tree.delete(item)
        
        aulas = db.listar_aulas()
        turmas = {t.id: t.nome_disciplina for t in db.listar_turmas()}
        professores = {p.id: p.nome for p in db.listar_professores()}
        
        for aula in aulas:
            turma_nome = turmas.get(aula.id_turma, "Desconhecida")
            prof_nome = professores.get(aula.id_professor, "Desconhecido")
            self.aulas_tree.insert('', 'end', 
                                  values=(aula.id, turma_nome, aula.data, aula.topico, prof_nome))
    
    def registrar_aula_adm(self):
        """Janela para registrar uma nova aula"""
        janela = tk.Toplevel(self.root)
        janela.title("Registrar Nova Aula")
        janela.geometry("400x300")
        janela.resizable(False, False)
        janela.grab_set()
        
        frame = tk.Frame(janela, bg=self.colors['white'])
        frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Turma
        tk.Label(frame, text="Turma:", bg=self.colors['white'],
                font=('Segoe UI', 10)).pack(pady=5)
        turmas = db.listar_turmas()
        turmas_opcoes = [f"{t.id} - {t.nome_disciplina}" for t in turmas]
        turma_combo = ttk.Combobox(frame, values=turmas_opcoes,
                                  font=('Segoe UI', 9), width=35, state='readonly')
        turma_combo.pack(pady=5)
        
        # Data
        tk.Label(frame, text="Data (dd/mm/yyyy):", bg=self.colors['white'],
                font=('Segoe UI', 10)).pack(pady=5)
        data_entry = tk.Entry(frame, font=('Segoe UI', 10), width=37)
        data_entry.insert(0, datetime.now().strftime('%d/%m/%Y'))
        data_entry.pack(pady=5)
        
        # Tópico
        tk.Label(frame, text="Tópico da Aula:", bg=self.colors['white'],
                font=('Segoe UI', 10)).pack(pady=5)
        topico_entry = tk.Entry(frame, font=('Segoe UI', 10), width=37)
        topico_entry.pack(pady=5)
        
        def salvar():
            if not turma_combo.get() or not topico_entry.get():
                messagebox.showwarning("Campos vazios", "Preencha todos os campos!", parent=janela)
                return
            
            id_turma = turma_combo.get().split(' - ')[0]
            data = data_entry.get()
            topico = topico_entry.get()
            
            novo_id = db.get_proximo_id(db.ARQUIVO_AULAS)
            aula = Aula(id=novo_id, id_turma=id_turma, data=data, 
                       topico=topico, id_professor=self.usuario_id)
            db.salvar_aula(aula)
            
            messagebox.showinfo("Sucesso", "Aula registrada com sucesso!", parent=janela)
            janela.destroy()
            self.listar_aulas_table()
        
        tk.Button(frame, text="Registrar Aula", bg=self.colors['success'],
                 fg=self.colors['white'], font=('Segoe UI', 10, 'bold'),
                 relief='flat', cursor='hand2',
                 command=salvar).pack(pady=15, ipadx=20, ipady=5)
    
    def criar_aba_atividades_adm(self, parent):
        """Cria a aba de atividades e notas"""
        # Dividir em dois frames: esquerda (atividades) e direita (notas)
        paned = tk.PanedWindow(parent, orient='horizontal', bg=self.colors['white'])
        paned.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Frame esquerdo - Atividades
        frame_ativ = tk.Frame(paned, bg=self.colors['white'])
        paned.add(frame_ativ, width=400)
        
        tk.Label(frame_ativ, text="Atividades", font=('Segoe UI', 12, 'bold'),
                bg=self.colors['white']).pack(pady=5)
        
        btn_frame = tk.Frame(frame_ativ, bg=self.colors['white'])
        btn_frame.pack(fill='x', padx=5, pady=5)
        
        tk.Button(btn_frame, text="Nova Atividade", bg=self.colors['accent'],
                 fg=self.colors['white'], font=('Segoe UI', 9),
                 relief='flat', cursor='hand2',
                 command=self.registrar_atividade).pack(side='left', padx=5, ipady=3, ipadx=8)
        
        tk.Button(btn_frame, text="Atualizar", bg=self.colors['success'],
                 fg=self.colors['white'], font=('Segoe UI', 9),
                 relief='flat', cursor='hand2',
                 command=self.listar_atividades_table).pack(side='right', padx=5, ipady=3, ipadx=8)
        
        # Treeview atividades
        tree_frame = tk.Frame(frame_ativ)
        tree_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        scrollbar = tk.Scrollbar(tree_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.atividades_tree = ttk.Treeview(tree_frame,
                                           columns=('ID', 'Turma', 'Descrição'),
                                           show='headings',
                                           yscrollcommand=scrollbar.set)
        
        self.atividades_tree.heading('ID', text='ID')
        self.atividades_tree.heading('Turma', text='Turma')
        self.atividades_tree.heading('Descrição', text='Descrição')
        
        self.atividades_tree.column('ID', width=40)
        self.atividades_tree.column('Turma', width=100)
        self.atividades_tree.column('Descrição', width=200)
        
        scrollbar.config(command=self.atividades_tree.yview)
        self.atividades_tree.pack(fill='both', expand=True)
        
        # Frame direito - Notas
        frame_notas = tk.Frame(paned, bg=self.colors['white'])
        paned.add(frame_notas, width=450)
        
        tk.Label(frame_notas, text="Gerenciar Notas", font=('Segoe UI', 12, 'bold'),
                bg=self.colors['white']).pack(pady=5)
        
        btn_frame2 = tk.Frame(frame_notas, bg=self.colors['white'])
        btn_frame2.pack(fill='x', padx=5, pady=5)
        
        tk.Button(btn_frame2, text="Lançar/Editar Nota", bg=self.colors['accent'],
                 fg=self.colors['white'], font=('Segoe UI', 9),
                 relief='flat', cursor='hand2',
                 command=self.lancar_nota).pack(side='left', padx=5, ipady=3, ipadx=8)
        
        tk.Button(btn_frame2, text="Ver Notas de Aluno", bg=self.colors['accent'],
                 fg=self.colors['white'], font=('Segoe UI', 9),
                 relief='flat', cursor='hand2',
                 command=self.visualizar_notas_aluno_gui).pack(side='left', padx=5, ipady=3, ipadx=8)
        
        info_label = tk.Label(frame_notas, 
                             text="Selecione as opções acima para gerenciar notas",
                             font=('Segoe UI', 10), bg=self.colors['white'],
                             fg=self.colors['secondary'])
        info_label.pack(expand=True)
        
        self.listar_atividades_table()
    
    def listar_atividades_table(self):
        """Carrega atividades na tabela"""
        for item in self.atividades_tree.get_children():
            self.atividades_tree.delete(item)
        
        atividades = db.listar_atividades()
        turmas = {t.id: t.nome_disciplina for t in db.listar_turmas()}
        
        for ativ in atividades:
            turma_nome = turmas.get(ativ.id_turma, "Desconhecida")
            self.atividades_tree.insert('', 'end',
                                       values=(ativ.id, turma_nome, ativ.descricao))
    
    def registrar_atividade(self):
        """Janela para registrar nova atividade"""
        janela = tk.Toplevel(self.root)
        janela.title("Registrar Nova Atividade")
        janela.geometry("400x250")
        janela.resizable(False, False)
        janela.grab_set()
        
        frame = tk.Frame(janela, bg=self.colors['white'])
        frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(frame, text="Turma:", bg=self.colors['white'],
                font=('Segoe UI', 10)).pack(pady=5)
        
        turmas = db.listar_turmas()
        turmas_opcoes = [f"{t.id} - {t.nome_disciplina}" for t in turmas]
        turma_combo = ttk.Combobox(frame, values=turmas_opcoes,
                                  font=('Segoe UI', 9), width=35, state='readonly')
        turma_combo.pack(pady=5)
        
        tk.Label(frame, text="Descrição da Atividade:", bg=self.colors['white'],
                font=('Segoe UI', 10)).pack(pady=5)
        desc_entry = tk.Entry(frame, font=('Segoe UI', 10), width=37)
        desc_entry.pack(pady=5)
        
        def salvar():
            if not turma_combo.get() or not desc_entry.get():
                messagebox.showwarning("Campos vazios", "Preencha todos os campos!", parent=janela)
                return
            
            id_turma = turma_combo.get().split(' - ')[0]
            descricao = desc_entry.get()
            
            novo_id = db.get_proximo_id(db.ARQUIVO_ATIVIDADES)
            # ADM não tem id_professor específico, deixa None
            atividade = Atividade(id=novo_id, id_turma=id_turma, descricao=descricao, id_professor=None)
            db.salvar_atividade(atividade)
            
            messagebox.showinfo("Sucesso", "Atividade registrada!", parent=janela)
            janela.destroy()
            self.listar_atividades_table()
        
        tk.Button(frame, text="Registrar", bg=self.colors['success'],
                 fg=self.colors['white'], font=('Segoe UI', 10, 'bold'),
                 relief='flat', cursor='hand2',
                 command=salvar).pack(pady=15, ipadx=30, ipady=5)
    
    def lancar_nota(self):
        """Janela para lançar/editar nota"""
        janela = tk.Toplevel(self.root)
        janela.title("Lançar/Editar Nota")
        janela.geometry("450x350")
        janela.resizable(False, False)
        janela.grab_set()
        
        frame = tk.Frame(janela, bg=self.colors['white'])
        frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Turma
        tk.Label(frame, text="Turma:", bg=self.colors['white'],
                font=('Segoe UI', 10)).grid(row=0, column=0, sticky='w', pady=5)
        turmas = db.listar_turmas()
        turmas_opcoes = [f"{t.id} - {t.nome_disciplina}" for t in turmas]
        turma_combo = ttk.Combobox(frame, values=turmas_opcoes,
                                  font=('Segoe UI', 9), width=30, state='readonly')
        turma_combo.grid(row=0, column=1, pady=5)
        
        # Aluno (será populado após selecionar turma)
        tk.Label(frame, text="Aluno:", bg=self.colors['white'],
                font=('Segoe UI', 10)).grid(row=1, column=0, sticky='w', pady=5)
        aluno_combo = ttk.Combobox(frame, font=('Segoe UI', 9), width=30, state='readonly')
        aluno_combo.grid(row=1, column=1, pady=5)
        
        # Atividade (será populado após selecionar turma)
        tk.Label(frame, text="Atividade:", bg=self.colors['white'],
                font=('Segoe UI', 10)).grid(row=2, column=0, sticky='w', pady=5)
        ativ_combo = ttk.Combobox(frame, font=('Segoe UI', 9), width=30, state='readonly')
        ativ_combo.grid(row=2, column=1, pady=5)
        
        # Nota
        tk.Label(frame, text="Nota:", bg=self.colors['white'],
                font=('Segoe UI', 10)).grid(row=3, column=0, sticky='w', pady=5)
        nota_entry = tk.Entry(frame, font=('Segoe UI', 10), width=32)
        nota_entry.grid(row=3, column=1, pady=5)
        
        def atualizar_alunos_atividades(event):
            if not turma_combo.get():
                return
            
            id_turma = turma_combo.get().split(' - ')[0]
            turma = db.buscar_turma_por_id(id_turma)
            
            # Atualizar alunos
            alunos = [al for al in db.listar_alunos() if al.id in turma.id_alunos]
            alunos_opcoes = [f"{a.id} - {a.nome}" for a in alunos]
            aluno_combo['values'] = alunos_opcoes
            
            # Atualizar atividades
            atividades = [atv for atv in db.listar_atividades() if atv.id_turma == id_turma]
            ativ_opcoes = [f"{a.id} - {a.descricao}" for a in atividades]
            ativ_combo['values'] = ativ_opcoes
        
        turma_combo.bind('<<ComboboxSelected>>', atualizar_alunos_atividades)
        
        def salvar():
            if not aluno_combo.get() or not ativ_combo.get() or not nota_entry.get():
                messagebox.showwarning("Campos vazios", "Preencha todos os campos!", parent=janela)
                return
            
            try:
                nota_valor = float(nota_entry.get())
            except ValueError:
                messagebox.showerror("Erro", "Nota inválida! Digite um número.", parent=janela)
                return
            
            id_aluno = aluno_combo.get().split(' - ')[0]
            id_atividade = ativ_combo.get().split(' - ')[0]
            
            nota = Nota(id_aluno=id_aluno, id_atividade=id_atividade, nota=nota_valor)
            db.salvar_ou_atualizar_nota(nota)
            
            messagebox.showinfo("Sucesso", "Nota salva com sucesso!", parent=janela)
            janela.destroy()
        
        tk.Button(frame, text="Salvar Nota", bg=self.colors['success'],
                 fg=self.colors['white'], font=('Segoe UI', 10, 'bold'),
                 relief='flat', cursor='hand2',
                 command=salvar).grid(row=4, column=0, columnspan=2, pady=20, ipadx=30, ipady=5)
    
    def visualizar_notas_aluno_gui(self):
        """Janela para visualizar notas de um aluno"""
        janela = tk.Toplevel(self.root)
        janela.title("Visualizar Notas de Aluno")
        janela.geometry("600x400")
        janela.resizable(False, False)
        janela.grab_set()
        
        frame_top = tk.Frame(janela, bg=self.colors['white'])
        frame_top.pack(fill='x', padx=20, pady=10)
        
        # Turma
        tk.Label(frame_top, text="Turma:", bg=self.colors['white'],
                font=('Segoe UI', 10)).grid(row=0, column=0, sticky='w', pady=5)
        turmas = db.listar_turmas()
        turmas_opcoes = [f"{t.id} - {t.nome_disciplina}" for t in turmas]
        turma_combo = ttk.Combobox(frame_top, values=turmas_opcoes,
                                  font=('Segoe UI', 9), width=30, state='readonly')
        turma_combo.grid(row=0, column=1, pady=5)
        
        # Aluno
        tk.Label(frame_top, text="Aluno:", bg=self.colors['white'],
                font=('Segoe UI', 10)).grid(row=1, column=0, sticky='w', pady=5)
        aluno_combo = ttk.Combobox(frame_top, font=('Segoe UI', 9), width=30, state='readonly')
        aluno_combo.grid(row=1, column=1, pady=5)
        
        def atualizar_alunos(event):
            if not turma_combo.get():
                return
            id_turma = turma_combo.get().split(' - ')[0]
            turma = db.buscar_turma_por_id(id_turma)
            alunos = [al for al in db.listar_alunos(filter_ativos=False) if al.id in turma.id_alunos]
            alunos_opcoes = [f"{a.id} - {a.nome}" for a in alunos]
            aluno_combo['values'] = alunos_opcoes
        
        turma_combo.bind('<<ComboboxSelected>>', atualizar_alunos)
        
        # Text widget para exibir notas
        frame_text = tk.Frame(janela, bg=self.colors['white'])
        frame_text.pack(fill='both', expand=True, padx=20, pady=10)
        
        text_scroll = tk.Scrollbar(frame_text)
        text_scroll.pack(side='right', fill='y')
        
        notas_text = tk.Text(frame_text, font=('Consolas', 10),
                            yscrollcommand=text_scroll.set,
                            wrap='word', state='disabled')
        notas_text.pack(fill='both', expand=True)
        text_scroll.config(command=notas_text.yview)
        
        def buscar_notas():
            if not aluno_combo.get():
                messagebox.showwarning("Seleção vazia", "Selecione um aluno!", parent=janela)
                return
            
            id_aluno = aluno_combo.get().split(' - ')[0]
            aluno = db.buscar_aluno_por_id(id_aluno)
            notas = db.listar_notas_por_aluno(id_aluno)
            atividades = {atv.id: atv for atv in db.listar_atividades()}
            
            notas_text.config(state='normal')
            notas_text.delete('1.0', 'end')
            
            notas_text.insert('end', f"=== Notas de {aluno.nome} (RA: {aluno.ra}) ===\n\n")
            
            if not notas:
                notas_text.insert('end', "Nenhuma nota encontrada.\n")
            else:
                soma = 0
                for nota in notas:
                    ativ = atividades.get(nota.id_atividade)
                    desc = ativ.descricao if ativ else "Desconhecida"
                    notas_text.insert('end', f"• {desc}: {nota.nota}\n")
                    soma += nota.nota
                
                media = soma / len(notas)
                notas_text.insert('end', f"\n{'='*40}\n")
                notas_text.insert('end', f"Média: {media:.2f}\n")
            
            notas_text.config(state='disabled')
        
        tk.Button(frame_top, text="Buscar Notas", bg=self.colors['accent'],
                 fg=self.colors['white'], font=('Segoe UI', 10),
                 relief='flat', cursor='hand2',
                 command=buscar_notas).grid(row=2, column=0, columnspan=2, pady=10, ipadx=20, ipady=5)
    
    def criar_aba_chamadas_adm(self, parent):
        """Cria a aba de gerenciamento de chamadas"""
        btn_frame = tk.Frame(parent, bg=self.colors['white'])
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(btn_frame, text="Registrar Chamada",
                 bg=self.colors['accent'], fg=self.colors['white'],
                 font=('Segoe UI', 10), relief='flat', cursor='hand2',
                 command=self.registrar_chamada_gui).pack(side='left', padx=5, ipady=5, ipadx=10)
        
        tk.Button(btn_frame, text="Editar Chamada",
                 bg=self.colors['warning'], fg=self.colors['white'],
                 font=('Segoe UI', 10), relief='flat', cursor='hand2',
                 command=self.editar_chamada_gui).pack(side='left', padx=5, ipady=5, ipadx=10)
        
        tk.Button(btn_frame, text="Visualizar Chamada",
                 bg=self.colors['accent'], fg=self.colors['white'],
                 font=('Segoe UI', 10), relief='flat', cursor='hand2',
                 command=self.visualizar_chamada_gui).pack(side='left', padx=5, ipady=5, ipadx=10)
        
        info_label = tk.Label(parent,
                             text="Selecione uma das opções acima para gerenciar chamadas",
                             font=('Segoe UI', 12), bg=self.colors['white'],
                             fg=self.colors['secondary'])
        info_label.pack(expand=True)
    
    def registrar_chamada_gui(self):
        """Interface para registrar chamada"""
        # Determinar se é professor ou ADM
        if self.usuario_papel == 'professor':
            aulas = [a for a in db.listar_aulas() if a.id_professor == str(self.usuario_id)]
        else:
            aulas = db.listar_aulas()
        
        if not aulas:
            messagebox.showwarning("Sem aulas", "Nenhuma aula registrada para fazer chamada.")
            return
        
        janela = tk.Toplevel(self.root)
        janela.title("Registrar Chamada")
        janela.geometry("700x500")
        janela.resizable(False, False)
        janela.grab_set()
        
        frame = tk.Frame(janela, bg=self.colors['white'])
        frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Seleção da aula
        tk.Label(frame, text="Selecione a Aula:", bg=self.colors['white'],
                font=('Segoe UI', 11, 'bold')).pack(pady=5)
        
        turmas = {t.id: t.nome_disciplina for t in db.listar_turmas()}
        aulas_opcoes = [f"ID {a.id} - {turmas.get(a.id_turma, 'Desconhecida')} - {a.data} - {a.topico}" 
                       for a in aulas]
        
        aula_combo = ttk.Combobox(frame, values=aulas_opcoes,
                                 font=('Segoe UI', 9), width=70, state='readonly')
        aula_combo.pack(pady=5)
        
        # Frame para lista de alunos
        tk.Label(frame, text="Marque a presença dos alunos:", bg=self.colors['white'],
                font=('Segoe UI', 11, 'bold')).pack(pady=(15, 5))
        
        info_label = tk.Label(frame, text="Selecione uma aula para carregar os alunos",
                             font=('Segoe UI', 9), bg=self.colors['white'],
                             fg=self.colors['secondary'])
        info_label.pack(pady=5)
        
        # Frame com scrollbar para alunos
        alunos_frame = tk.Frame(frame, bg=self.colors['white'])
        alunos_frame.pack(fill='both', expand=True, pady=10)
        
        canvas = tk.Canvas(alunos_frame, bg=self.colors['white'])
        scrollbar = tk.Scrollbar(alunos_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['white'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        chamada_vars = {}  # Dicionário para armazenar as variáveis dos checkboxes
        
        def carregar_alunos(event):
            # Limpar frame
            for widget in scrollable_frame.winfo_children():
                widget.destroy()
            chamada_vars.clear()
            
            if not aula_combo.get():
                return
            
            # Pegar ID da aula selecionada
            id_aula = aula_combo.get().split(' - ')[0].replace('ID ', '')
            aula_selecionada = next((a for a in aulas if a.id == id_aula), None)
            
            if not aula_selecionada:
                return
            
            # Verificar se já existe chamada
            if db.listar_chamadas_por_aula(id_aula):
                info_label.config(text="⚠ Esta aula já possui chamada registrada! Use 'Editar Chamada'.",
                                fg=self.colors['danger'])
                return
            else:
                info_label.config(text="✓ Marque os alunos presentes (desmarcados = falta)",
                                fg=self.colors['success'])
            
            # Carregar alunos da turma
            turma = db.buscar_turma_por_id(aula_selecionada.id_turma)
            if not turma or not turma.id_alunos:
                tk.Label(scrollable_frame, text="Nenhum aluno nesta turma",
                        bg=self.colors['white'], font=('Segoe UI', 10)).pack(pady=20)
                return
            
            todos_alunos = {al.id: al for al in db.listar_alunos()}
            
            for id_aluno in turma.id_alunos:
                if id_aluno in todos_alunos:
                    aluno = todos_alunos[id_aluno]
                    var = tk.BooleanVar(value=True)  # Presente por padrão
                    chamada_vars[id_aluno] = var
                    
                    cb = tk.Checkbutton(scrollable_frame,
                                       text=f"{aluno.nome} (RA: {aluno.ra})",
                                       variable=var,
                                       font=('Segoe UI', 10),
                                       bg=self.colors['white'],
                                       activebackground=self.colors['white'])
                    cb.pack(anchor='w', pady=3, padx=10)
        
        aula_combo.bind('<<ComboboxSelected>>', carregar_alunos)
        
        # Botões
        btn_frame = tk.Frame(frame, bg=self.colors['white'])
        btn_frame.pack(pady=10)
        
        def salvar_chamada():
            if not aula_combo.get():
                messagebox.showwarning("Aula não selecionada", 
                                     "Selecione uma aula!", parent=janela)
                return
            
            if not chamada_vars:
                messagebox.showwarning("Sem alunos", 
                                     "Carregue os alunos primeiro!", parent=janela)
                return
            
            id_aula = aula_combo.get().split(' - ')[0].replace('ID ', '')
            
            # Criar lista de chamadas
            lista_chamadas = []
            for id_aluno, var in chamada_vars.items():
                status = 'P' if var.get() else 'F'
                lista_chamadas.append(Chamada(id_aula=id_aula, id_aluno=id_aluno, status=status))
            
            db.salvar_chamada(lista_chamadas)
            messagebox.showinfo("Sucesso", 
                              f"Chamada registrada com {sum(1 for v in chamada_vars.values() if v.get())} presentes!",
                              parent=janela)
            janela.destroy()
        
        tk.Button(btn_frame, text="Salvar Chamada", bg=self.colors['success'],
                 fg=self.colors['white'], font=('Segoe UI', 10, 'bold'),
                 relief='flat', cursor='hand2',
                 command=salvar_chamada).pack(side='left', padx=5, ipadx=30, ipady=8)
        
        tk.Button(btn_frame, text="Cancelar", bg=self.colors['secondary'],
                 fg=self.colors['white'], font=('Segoe UI', 10),
                 relief='flat', cursor='hand2',
                 command=janela.destroy).pack(side='left', padx=5, ipadx=30, ipady=8)
    
    def editar_chamada_gui(self):
        """Interface para editar chamada existente"""
        # Determinar se é professor ou ADM
        if self.usuario_papel == 'professor':
            aulas = [a for a in db.listar_aulas() if a.id_professor == str(self.usuario_id)]
        else:
            aulas = db.listar_aulas()
        
        # Filtrar apenas aulas que já têm chamada
        aulas_com_chamada = [a for a in aulas if db.listar_chamadas_por_aula(a.id)]
        
        if not aulas_com_chamada:
            messagebox.showwarning("Sem chamadas", 
                                 "Nenhuma aula possui chamada registrada para editar.")
            return
        
        janela = tk.Toplevel(self.root)
        janela.title("Editar Chamada")
        janela.geometry("700x500")
        janela.resizable(False, False)
        janela.grab_set()
        
        frame = tk.Frame(janela, bg=self.colors['white'])
        frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Seleção da aula
        tk.Label(frame, text="Selecione a Aula para Editar:", bg=self.colors['white'],
                font=('Segoe UI', 11, 'bold')).pack(pady=5)
        
        turmas = {t.id: t.nome_disciplina for t in db.listar_turmas()}
        aulas_opcoes = [f"ID {a.id} - {turmas.get(a.id_turma, 'Desconhecida')} - {a.data} - {a.topico}" 
                       for a in aulas_com_chamada]
        
        aula_combo = ttk.Combobox(frame, values=aulas_opcoes,
                                 font=('Segoe UI', 9), width=70, state='readonly')
        aula_combo.pack(pady=5)
        
        # Frame para lista de alunos
        tk.Label(frame, text="Edite a presença dos alunos:", bg=self.colors['white'],
                font=('Segoe UI', 11, 'bold')).pack(pady=(15, 5))
        
        info_label = tk.Label(frame, text="Selecione uma aula para carregar a chamada",
                             font=('Segoe UI', 9), bg=self.colors['white'],
                             fg=self.colors['secondary'])
        info_label.pack(pady=5)
        
        # Frame com scrollbar para alunos
        alunos_frame = tk.Frame(frame, bg=self.colors['white'])
        alunos_frame.pack(fill='both', expand=True, pady=10)
        
        canvas = tk.Canvas(alunos_frame, bg=self.colors['white'])
        scrollbar = tk.Scrollbar(alunos_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['white'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        chamada_vars = {}
        
        def carregar_chamada(event):
            for widget in scrollable_frame.winfo_children():
                widget.destroy()
            chamada_vars.clear()
            
            if not aula_combo.get():
                return
            
            id_aula = aula_combo.get().split(' - ')[0].replace('ID ', '')
            aula_selecionada = next((a for a in aulas_com_chamada if a.id == id_aula), None)
            
            if not aula_selecionada:
                return
            
            info_label.config(text="✓ Edite a chamada conforme necessário",
                            fg=self.colors['accent'])
            
            # Carregar chamada existente
            chamadas_existentes = db.listar_chamadas_por_aula(id_aula)
            chamada_map = {c.id_aluno: c.status for c in chamadas_existentes}
            
            # Carregar alunos
            turma = db.buscar_turma_por_id(aula_selecionada.id_turma)
            todos_alunos = {al.id: al for al in db.listar_alunos(filter_ativos=False)}
            
            for id_aluno in turma.id_alunos:
                if id_aluno in todos_alunos:
                    aluno = todos_alunos[id_aluno]
                    status_atual = chamada_map.get(id_aluno, 'F')
                    var = tk.BooleanVar(value=(status_atual == 'P'))
                    chamada_vars[id_aluno] = var
                    
                    cb = tk.Checkbutton(scrollable_frame,
                                       text=f"{aluno.nome} (RA: {aluno.ra})",
                                       variable=var,
                                       font=('Segoe UI', 10),
                                       bg=self.colors['white'],
                                       activebackground=self.colors['white'])
                    cb.pack(anchor='w', pady=3, padx=10)
        
        aula_combo.bind('<<ComboboxSelected>>', carregar_chamada)
        
        # Botões
        btn_frame = tk.Frame(frame, bg=self.colors['white'])
        btn_frame.pack(pady=10)
        
        def salvar_edicao():
            if not aula_combo.get():
                messagebox.showwarning("Aula não selecionada", 
                                     "Selecione uma aula!", parent=janela)
                return
            
            if not chamada_vars:
                messagebox.showwarning("Sem dados", 
                                     "Carregue a chamada primeiro!", parent=janela)
                return
            
            id_aula = aula_combo.get().split(' - ')[0].replace('ID ', '')
            
            # Criar nova lista de chamadas
            nova_lista = []
            for id_aluno, var in chamada_vars.items():
                status = 'P' if var.get() else 'F'
                nova_lista.append(Chamada(id_aula=id_aula, id_aluno=id_aluno, status=status))
            
            db.sobrescrever_chamada_por_aula(id_aula, nova_lista)
            messagebox.showinfo("Sucesso", "Chamada atualizada com sucesso!", parent=janela)
            janela.destroy()
        
        tk.Button(btn_frame, text="Salvar Alterações", bg=self.colors['warning'],
                 fg=self.colors['white'], font=('Segoe UI', 10, 'bold'),
                 relief='flat', cursor='hand2',
                 command=salvar_edicao).pack(side='left', padx=5, ipadx=30, ipady=8)
        
        tk.Button(btn_frame, text="Cancelar", bg=self.colors['secondary'],
                 fg=self.colors['white'], font=('Segoe UI', 10),
                 relief='flat', cursor='hand2',
                 command=janela.destroy).pack(side='left', padx=5, ipadx=30, ipady=8)
    
    def visualizar_chamada_gui(self):
        """Interface para visualizar chamada de uma aula"""
        # Determinar se é professor ou ADM
        if self.usuario_papel == 'professor':
            turmas = self.obter_turmas_professor()
        else:
            turmas = db.listar_turmas()
        
        if not turmas:
            messagebox.showwarning("Sem turmas", "Nenhuma turma disponível.")
            return
        
        janela = tk.Toplevel(self.root)
        janela.title("Visualizar Chamada")
        janela.geometry("700x550")
        janela.resizable(False, False)
        janela.grab_set()
        
        frame = tk.Frame(janela, bg=self.colors['white'])
        frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Seleção da turma
        tk.Label(frame, text="1. Selecione a Turma:", bg=self.colors['white'],
                font=('Segoe UI', 11, 'bold')).pack(pady=5)
        
        turmas_opcoes = [f"{t.id} - {t.nome_disciplina}" for t in turmas]
        turma_combo = ttk.Combobox(frame, values=turmas_opcoes,
                                  font=('Segoe UI', 9), width=50, state='readonly')
        turma_combo.pack(pady=5)
        
        # Seleção da aula
        tk.Label(frame, text="2. Selecione a Aula:", bg=self.colors['white'],
                font=('Segoe UI', 11, 'bold')).pack(pady=(15, 5))
        
        aula_combo = ttk.Combobox(frame, font=('Segoe UI', 9), width=50, state='readonly')
        aula_combo.pack(pady=5)
        
        # Tabela para mostrar chamada
        tk.Label(frame, text="3. Chamada da Aula:", bg=self.colors['white'],
                font=('Segoe UI', 11, 'bold')).pack(pady=(15, 5))
        
        table_frame = tk.Frame(frame, bg=self.colors['white'])
        table_frame.pack(fill='both', expand=True, pady=10)
        
        scrollbar = tk.Scrollbar(table_frame)
        scrollbar.pack(side='right', fill='y')
        
        chamada_tree = ttk.Treeview(table_frame,
                                    columns=('Aluno', 'RA', 'Status'),
                                    show='headings',
                                    yscrollcommand=scrollbar.set,
                                    height=10)
        
        chamada_tree.heading('Aluno', text='Aluno')
        chamada_tree.heading('RA', text='RA')
        chamada_tree.heading('Status', text='Status')
        
        chamada_tree.column('Aluno', width=300)
        chamada_tree.column('RA', width=100)
        chamada_tree.column('Status', width=150)
        
        scrollbar.config(command=chamada_tree.yview)
        chamada_tree.pack(fill='both', expand=True)
        
        # Label para estatísticas
        stats_label = tk.Label(frame, text="", font=('Segoe UI', 10, 'bold'),
                              bg=self.colors['white'], fg=self.colors['primary'])
        stats_label.pack(pady=10)
        
        def atualizar_aulas(event):
            if not turma_combo.get():
                return
            
            id_turma = turma_combo.get().split(' - ')[0]
            
            # Filtrar aulas da turma
            if self.usuario_papel == 'professor':
                aulas = [a for a in db.listar_aulas() 
                        if a.id_turma == id_turma and a.id_professor == str(self.usuario_id)]
            else:
                aulas = [a for a in db.listar_aulas() if a.id_turma == id_turma]
            
            professores = {p.id: p.nome for p in db.listar_professores()}
            aulas_opcoes = [f"ID {a.id} - {a.data} - {a.topico} - Prof: {professores.get(a.id_professor, 'Desconhecido')}" 
                           for a in aulas]
            
            aula_combo['values'] = aulas_opcoes
            aula_combo.set('')
            
            # Limpar tabela
            for item in chamada_tree.get_children():
                chamada_tree.delete(item)
            stats_label.config(text="")
        
        def visualizar_chamada(event):
            if not aula_combo.get():
                return
            
            # Limpar tabela
            for item in chamada_tree.get_children():
                chamada_tree.delete(item)
            
            id_aula = aula_combo.get().split(' - ')[0].replace('ID ', '')
            
            chamadas = db.listar_chamadas_por_aula(id_aula)
            
            if not chamadas:
                chamada_tree.insert('', 'end', values=('Nenhuma chamada registrada', '', ''))
                stats_label.config(text="")
                return
            
            # Carregar alunos
            alunos = {al.id: al for al in db.listar_alunos(filter_ativos=False)}
            
            presentes = 0
            faltas = 0
            
            for chamada in chamadas:
                aluno = alunos.get(chamada.id_aluno)
                if aluno:
                    status_text = "✓ Presente" if chamada.status == 'P' else "✗ Falta"
                    chamada_tree.insert('', 'end', 
                                       values=(aluno.nome, aluno.ra, status_text))
                    
                    if chamada.status == 'P':
                        presentes += 1
                    else:
                        faltas += 1
            
            total = presentes + faltas
            if total > 0:
                percentual = (presentes / total) * 100
                stats_label.config(
                    text=f"Presentes: {presentes} | Faltas: {faltas} | Frequência: {percentual:.1f}%"
                )
        
        turma_combo.bind('<<ComboboxSelected>>', atualizar_aulas)
        aula_combo.bind('<<ComboboxSelected>>', visualizar_chamada)
        
        # Botão fechar
        tk.Button(frame, text="Fechar", bg=self.colors['secondary'],
                 fg=self.colors['white'], font=('Segoe UI', 10),
                 relief='flat', cursor='hand2',
                 command=janela.destroy).pack(pady=10, ipadx=30, ipady=8)
    
    def mostrar_menu_professor(self):
        """Exibe o menu principal do professor com abas"""
        self.limpar_janela()
        self.criar_header(self.root)
        
        main_frame = tk.Frame(self.root, bg=self.colors['light'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill='both', expand=True)
        
        # Aba 1: Minhas Turmas
        tab_turmas = tk.Frame(notebook, bg=self.colors['white'])
        notebook.add(tab_turmas, text='Minhas Turmas')
        self.criar_aba_turmas_professor(tab_turmas)
        
        # Aba 2: Minhas Aulas
        tab_aulas = tk.Frame(notebook, bg=self.colors['white'])
        notebook.add(tab_aulas, text='Minhas Aulas')
        self.criar_aba_aulas_professor(tab_aulas)
        
        # Aba 3: Atividades e Notas
        tab_atividades = tk.Frame(notebook, bg=self.colors['white'])
        notebook.add(tab_atividades, text='Atividades e Notas')
        self.criar_aba_atividades_professor(tab_atividades)
        
        # Aba 4: Chamadas
        tab_chamadas = tk.Frame(notebook, bg=self.colors['white'])
        notebook.add(tab_chamadas, text='Chamadas')
        self.criar_aba_chamadas_professor(tab_chamadas)
    
    def obter_turmas_professor(self):
        """Retorna as turmas associadas ao professor logado"""
        aulas_prof = [aula for aula in db.listar_aulas() if aula.id_professor == str(self.usuario_id)]
        ids_turmas = {aula.id_turma for aula in aulas_prof}
        return [turma for turma in db.listar_turmas() if turma.id in ids_turmas]
    
    def criar_aba_turmas_professor(self, parent):
        """Aba de turmas do professor"""
        btn_frame = tk.Frame(parent, bg=self.colors['white'])
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(btn_frame, text="Atualizar Lista",
                 bg=self.colors['success'], fg=self.colors['white'],
                 font=('Segoe UI', 10), relief='flat', cursor='hand2',
                 command=self.listar_turmas_professor_table).pack(side='right', padx=5, ipady=5, ipadx=10)
        
        # Tabela de turmas
        table_frame = tk.Frame(parent, bg=self.colors['white'])
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(table_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.turmas_prof_tree = ttk.Treeview(table_frame,
                                            columns=('ID', 'Turma', 'Qtd Alunos', 'Alunos'),
                                            show='headings',
                                            yscrollcommand=scrollbar.set)
        
        self.turmas_prof_tree.heading('ID', text='ID')
        self.turmas_prof_tree.heading('Turma', text='Turma')
        self.turmas_prof_tree.heading('Qtd Alunos', text='Qtd')
        self.turmas_prof_tree.heading('Alunos', text='Alunos')
        
        self.turmas_prof_tree.column('ID', width=50)
        self.turmas_prof_tree.column('Turma', width=150)
        self.turmas_prof_tree.column('Qtd Alunos', width=70)
        self.turmas_prof_tree.column('Alunos', width=430)
        
        scrollbar.config(command=self.turmas_prof_tree.yview)
        self.turmas_prof_tree.pack(fill='both', expand=True)
        
        self.listar_turmas_professor_table()
    
    def listar_turmas_professor_table(self):
        """Lista as turmas do professor"""
        for item in self.turmas_prof_tree.get_children():
            self.turmas_prof_tree.delete(item)
        
        turmas = self.obter_turmas_professor()
        todos_alunos = {al.id: al for al in db.listar_alunos()}
        
        if not turmas:
            self.turmas_prof_tree.insert('', 'end', 
                                        values=('', 'Nenhuma turma associada', '', 
                                               'Registre uma aula para se associar a uma turma'))
            return
        
        for turma in turmas:
            alunos_nomes = [todos_alunos[id_al].nome for id_al in turma.id_alunos if id_al in todos_alunos]
            alunos_str = ", ".join(alunos_nomes) if alunos_nomes else "Nenhum aluno"
            self.turmas_prof_tree.insert('', 'end',
                                        values=(turma.id, turma.nome_disciplina, 
                                               len(alunos_nomes), alunos_str))
    
    def criar_aba_aulas_professor(self, parent):
        """Aba de aulas do professor"""
        btn_frame = tk.Frame(parent, bg=self.colors['white'])
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(btn_frame, text="Registrar Nova Aula",
                 bg=self.colors['accent'], fg=self.colors['white'],
                 font=('Segoe UI', 10), relief='flat', cursor='hand2',
                 command=self.registrar_aula_professor).pack(side='left', padx=5, ipady=5, ipadx=10)
        
        tk.Button(btn_frame, text="Atualizar Lista",
                 bg=self.colors['success'], fg=self.colors['white'],
                 font=('Segoe UI', 10), relief='flat', cursor='hand2',
                 command=self.listar_aulas_professor_table).pack(side='right', padx=5, ipady=5, ipadx=10)
        
        # Tabela
        table_frame = tk.Frame(parent, bg=self.colors['white'])
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(table_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.aulas_prof_tree = ttk.Treeview(table_frame,
                                           columns=('ID', 'Turma', 'Data', 'Tópico'),
                                           show='headings',
                                           yscrollcommand=scrollbar.set)
        
        self.aulas_prof_tree.heading('ID', text='ID')
        self.aulas_prof_tree.heading('Turma', text='Turma')
        self.aulas_prof_tree.heading('Data', text='Data')
        self.aulas_prof_tree.heading('Tópico', text='Tópico')
        
        self.aulas_prof_tree.column('ID', width=50)
        self.aulas_prof_tree.column('Turma', width=150)
        self.aulas_prof_tree.column('Data', width=100)
        self.aulas_prof_tree.column('Tópico', width=400)
        
        scrollbar.config(command=self.aulas_prof_tree.yview)
        self.aulas_prof_tree.pack(fill='both', expand=True)
        
        self.listar_aulas_professor_table()
    
    def listar_aulas_professor_table(self):
        """Lista aulas do professor"""
        for item in self.aulas_prof_tree.get_children():
            self.aulas_prof_tree.delete(item)
        
        aulas = [a for a in db.listar_aulas() if a.id_professor == str(self.usuario_id)]
        turmas = {t.id: t.nome_disciplina for t in db.listar_turmas()}
        
        for aula in aulas:
            turma_nome = turmas.get(aula.id_turma, "Desconhecida")
            self.aulas_prof_tree.insert('', 'end',
                                       values=(aula.id, turma_nome, aula.data, aula.topico))
    
    def registrar_aula_professor(self):
        """Registra nova aula para o professor"""
        janela = tk.Toplevel(self.root)
        janela.title("Registrar Nova Aula")
        janela.geometry("400x300")
        janela.resizable(False, False)
        janela.grab_set()
        
        frame = tk.Frame(janela, bg=self.colors['white'])
        frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(frame, text="Turma:", bg=self.colors['white'],
                font=('Segoe UI', 10)).pack(pady=5)
        
        turmas = db.listar_turmas()
        turmas_opcoes = [f"{t.id} - {t.nome_disciplina}" for t in turmas]
        turma_combo = ttk.Combobox(frame, values=turmas_opcoes,
                                  font=('Segoe UI', 9), width=35, state='readonly')
        turma_combo.pack(pady=5)
        
        tk.Label(frame, text="Data (dd/mm/yyyy):", bg=self.colors['white'],
                font=('Segoe UI', 10)).pack(pady=5)
        data_entry = tk.Entry(frame, font=('Segoe UI', 10), width=37)
        data_entry.insert(0, datetime.now().strftime('%d/%m/%Y'))
        data_entry.pack(pady=5)
        
        tk.Label(frame, text="Tópico da Aula:", bg=self.colors['white'],
                font=('Segoe UI', 10)).pack(pady=5)
        topico_entry = tk.Entry(frame, font=('Segoe UI', 10), width=37)
        topico_entry.pack(pady=5)
        
        def salvar():
            if not turma_combo.get() or not topico_entry.get():
                messagebox.showwarning("Campos vazios", "Preencha todos os campos!", parent=janela)
                return
            
            id_turma = turma_combo.get().split(' - ')[0]
            data = data_entry.get()
            topico = topico_entry.get()
            
            novo_id = db.get_proximo_id(db.ARQUIVO_AULAS)
            aula = Aula(id=novo_id, id_turma=id_turma, data=data,
                       topico=topico, id_professor=self.usuario_id)
            db.salvar_aula(aula)
            
            messagebox.showinfo("Sucesso", "Aula registrada!", parent=janela)
            janela.destroy()
            self.listar_aulas_professor_table()
            self.listar_turmas_professor_table()
        
        tk.Button(frame, text="Registrar", bg=self.colors['success'],
                 fg=self.colors['white'], font=('Segoe UI', 10, 'bold'),
                 relief='flat', cursor='hand2',
                 command=salvar).pack(pady=15, ipadx=30, ipady=5)
    
    def criar_aba_atividades_professor(self, parent):
        """Aba de atividades do professor"""
        paned = tk.PanedWindow(parent, orient='horizontal', bg=self.colors['white'])
        paned.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Frame esquerdo - Atividades
        frame_ativ = tk.Frame(paned, bg=self.colors['white'])
        paned.add(frame_ativ, width=400)
        
        tk.Label(frame_ativ, text="Minhas Atividades", font=('Segoe UI', 12, 'bold'),
                bg=self.colors['white']).pack(pady=5)
        
        btn_frame = tk.Frame(frame_ativ, bg=self.colors['white'])
        btn_frame.pack(fill='x', padx=5, pady=5)
        
        tk.Button(btn_frame, text="Nova Atividade", bg=self.colors['accent'],
                 fg=self.colors['white'], font=('Segoe UI', 9),
                 relief='flat', cursor='hand2',
                 command=self.registrar_atividade_professor).pack(side='left', padx=5, ipady=3, ipadx=8)
        
        # Frame direito - Notas
        frame_notas = tk.Frame(paned, bg=self.colors['white'])
        paned.add(frame_notas, width=450)
        
        tk.Label(frame_notas, text="Gerenciar Notas", font=('Segoe UI', 12, 'bold'),
                bg=self.colors['white']).pack(pady=5)
        
        btn_frame2 = tk.Frame(frame_notas, bg=self.colors['white'])
        btn_frame2.pack(fill='x', padx=5, pady=5)
        
        tk.Button(btn_frame2, text="Lançar Nota", bg=self.colors['accent'],
                 fg=self.colors['white'], font=('Segoe UI', 9),
                 relief='flat', cursor='hand2',
                 command=self.lancar_nota_professor).pack(side='left', padx=5, ipady=3, ipadx=8)
        
        tk.Button(btn_frame2, text="Editar Nota", bg=self.colors['warning'],
                 fg=self.colors['white'], font=('Segoe UI', 9),
                 relief='flat', cursor='hand2',
                 command=self.editar_nota_professor).pack(side='left', padx=5, ipady=3, ipadx=8)
        
        tk.Button(btn_frame2, text="Ver Notas", bg=self.colors['accent'],
                 fg=self.colors['white'], font=('Segoe UI', 9),
                 relief='flat', cursor='hand2',
                 command=self.visualizar_notas_professor).pack(side='left', padx=5, ipady=3, ipadx=8)
    
    def registrar_atividade_professor(self):
        """Registra atividade nas turmas do professor"""
        turmas = self.obter_turmas_professor()
        if not turmas:
            messagebox.showwarning("Sem turmas", 
                                 "Você precisa registrar uma aula em uma turma primeiro.")
            return
        
        janela = tk.Toplevel(self.root)
        janela.title("Registrar Nova Atividade")
        janela.geometry("400x250")
        janela.resizable(False, False)
        janela.grab_set()
        
        frame = tk.Frame(janela, bg=self.colors['white'])
        frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(frame, text="Turma:", bg=self.colors['white'],
                font=('Segoe UI', 10)).pack(pady=5)
        
        turmas_opcoes = [f"{t.id} - {t.nome_disciplina}" for t in turmas]
        turma_combo = ttk.Combobox(frame, values=turmas_opcoes,
                                  font=('Segoe UI', 9), width=35, state='readonly')
        turma_combo.pack(pady=5)
        
        tk.Label(frame, text="Descrição da Atividade:", bg=self.colors['white'],
                font=('Segoe UI', 10)).pack(pady=5)
        desc_entry = tk.Entry(frame, font=('Segoe UI', 10), width=37)
        desc_entry.pack(pady=5)
        
        def salvar():
            if not turma_combo.get() or not desc_entry.get():
                messagebox.showwarning("Campos vazios", "Preencha todos os campos!", parent=janela)
                return
            
            id_turma = turma_combo.get().split(' - ')[0]
            descricao = desc_entry.get()
            
            novo_id = db.get_proximo_id(db.ARQUIVO_ATIVIDADES)
            # Atividade criada pelo professor logado
            atividade = Atividade(id=novo_id, id_turma=id_turma, descricao=descricao, 
                                id_professor=self.usuario_id)
            db.salvar_atividade(atividade)
            
            messagebox.showinfo("Sucesso", "Atividade registrada!", parent=janela)
            janela.destroy()
        
        tk.Button(frame, text="Registrar", bg=self.colors['success'],
                 fg=self.colors['white'], font=('Segoe UI', 10, 'bold'),
                 relief='flat', cursor='hand2',
                 command=salvar).pack(pady=15, ipadx=30, ipady=5)
    
    def lancar_nota_professor(self):
        """Lança nota APENAS para atividades criadas pelo professor (sem nota ainda)"""
        # Buscar atividades criadas pelo professor
        minhas_atividades = [atv for atv in db.listar_atividades() 
                            if atv.id_professor == str(self.usuario_id)]
        
        if not minhas_atividades:
            messagebox.showwarning("Sem atividades", 
                                 "Você não criou nenhuma atividade ainda.\nCrie uma atividade primeiro para poder lançar notas.")
            return
        
        janela = tk.Toplevel(self.root)
        janela.title("Lançar Nota - Apenas Minhas Atividades")
        janela.geometry("450x300")
        janela.resizable(False, False)
        janela.grab_set()
        
        frame = tk.Frame(janela, bg=self.colors['white'])
        frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Atividade - APENAS atividades do professor
        tk.Label(frame, text="Minha Atividade:", bg=self.colors['white'],
                font=('Segoe UI', 10)).grid(row=0, column=0, sticky='w', pady=5)
        
        turmas_dict = {t.id: t.nome_disciplina for t in db.listar_turmas()}
        ativ_opcoes = [f"{a.id} - {turmas_dict.get(a.id_turma, 'Turma?')} - {a.descricao}" 
                      for a in minhas_atividades]
        ativ_combo = ttk.Combobox(frame, values=ativ_opcoes,
                                 font=('Segoe UI', 9), width=40, state='readonly')
        ativ_combo.grid(row=0, column=1, pady=5)
        
        # Aluno
        tk.Label(frame, text="Aluno:", bg=self.colors['white'],
                font=('Segoe UI', 10)).grid(row=1, column=0, sticky='w', pady=5)
        aluno_combo = ttk.Combobox(frame, font=('Segoe UI', 9), width=40, state='readonly')
        aluno_combo.grid(row=1, column=1, pady=5)
        
        # Nota
        tk.Label(frame, text="Nota:", bg=self.colors['white'],
                font=('Segoe UI', 10)).grid(row=2, column=0, sticky='w', pady=5)
        nota_entry = tk.Entry(frame, font=('Segoe UI', 10), width=42)
        nota_entry.grid(row=2, column=1, pady=5)
        
        def carregar_alunos(event):
            if not ativ_combo.get():
                return
            
            id_atividade = ativ_combo.get().split(' - ')[0]
            atividade = next((a for a in minhas_atividades if a.id == id_atividade), None)
            
            if not atividade:
                return
            
            # Buscar turma da atividade
            turma = db.buscar_turma_por_id(atividade.id_turma)
            if not turma or not turma.id_alunos:
                messagebox.showwarning("Sem alunos", "Esta turma não tem alunos.", parent=janela)
                return
            
            # Carregar alunos
            alunos = [al for al in db.listar_alunos() if al.id in turma.id_alunos]
            alunos_opcoes = [f"{a.id} - {a.nome}" for a in alunos]
            aluno_combo['values'] = alunos_opcoes
        
        ativ_combo.bind('<<ComboboxSelected>>', carregar_alunos)
        
        def salvar():
            if not ativ_combo.get() or not aluno_combo.get() or not nota_entry.get():
                messagebox.showwarning("Campos vazios", "Preencha todos os campos!", parent=janela)
                return
            
            try:
                nota_valor = float(nota_entry.get())
            except ValueError:
                messagebox.showerror("Erro", "Nota inválida! Digite um número.", parent=janela)
                return
            
            id_atividade = ativ_combo.get().split(' - ')[0]
            id_aluno = aluno_combo.get().split(' - ')[0]
            
            # Verificar se já existe nota
            notas_existentes = db.listar_notas_por_aluno(id_aluno)
            if any(n.id_atividade == id_atividade for n in notas_existentes):
                messagebox.showwarning("Nota já existe", 
                                     "Este aluno já possui nota nesta atividade!\nUse 'Editar Nota' para alterar.",
                                     parent=janela)
                return
            
            nota = Nota(id_aluno=id_aluno, id_atividade=id_atividade, nota=nota_valor)
            db.salvar_ou_atualizar_nota(nota)
            
            messagebox.showinfo("Sucesso", "Nota lançada com sucesso!", parent=janela)
            # Limpar campos para próximo lançamento
            nota_entry.delete(0, 'end')
            aluno_combo.set('')
        
        tk.Button(frame, text="Lançar Nota", bg=self.colors['success'],
                 fg=self.colors['white'], font=('Segoe UI', 10, 'bold'),
                 relief='flat', cursor='hand2',
                 command=salvar).grid(row=3, column=0, columnspan=2, pady=20, ipadx=30, ipady=5)
    
    def editar_nota_professor(self):
        """Edita notas APENAS das atividades criadas pelo professor"""
        # Buscar atividades criadas pelo professor
        minhas_atividades = [atv for atv in db.listar_atividades() 
                            if atv.id_professor == str(self.usuario_id)]
        
        if not minhas_atividades:
            messagebox.showwarning("Sem atividades", 
                                 "Você não criou nenhuma atividade ainda.")
            return
        
        janela = tk.Toplevel(self.root)
        janela.title("Editar Nota - Apenas Minhas Atividades")
        janela.geometry("450x300")
        janela.resizable(False, False)
        janela.grab_set()
        
        frame = tk.Frame(janela, bg=self.colors['white'])
        frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Atividade
        tk.Label(frame, text="Minha Atividade:", bg=self.colors['white'],
                font=('Segoe UI', 10)).grid(row=0, column=0, sticky='w', pady=5)
        
        turmas_dict = {t.id: t.nome_disciplina for t in db.listar_turmas()}
        ativ_opcoes = [f"{a.id} - {turmas_dict.get(a.id_turma, 'Turma?')} - {a.descricao}" 
                      for a in minhas_atividades]
        ativ_combo = ttk.Combobox(frame, values=ativ_opcoes,
                                 font=('Segoe UI', 9), width=40, state='readonly')
        ativ_combo.grid(row=0, column=1, pady=5)
        
        # Aluno
        tk.Label(frame, text="Aluno:", bg=self.colors['white'],
                font=('Segoe UI', 10)).grid(row=1, column=0, sticky='w', pady=5)
        aluno_combo = ttk.Combobox(frame, font=('Segoe UI', 9), width=40, state='readonly')
        aluno_combo.grid(row=1, column=1, pady=5)
        
        # Nota
        tk.Label(frame, text="Nova Nota:", bg=self.colors['white'],
                font=('Segoe UI', 10)).grid(row=2, column=0, sticky='w', pady=5)
        nota_entry = tk.Entry(frame, font=('Segoe UI', 10), width=42)
        nota_entry.grid(row=2, column=1, pady=5)
        
        def carregar_alunos_com_nota(event):
            if not ativ_combo.get():
                return
            
            id_atividade = ativ_combo.get().split(' - ')[0]
            atividade = next((a for a in minhas_atividades if a.id == id_atividade), None)
            
            if not atividade:
                return
            
            # Buscar turma da atividade
            turma = db.buscar_turma_por_id(atividade.id_turma)
            if not turma or not turma.id_alunos:
                return
            
            # Carregar apenas alunos que JÁ TÊM nota nesta atividade
            alunos = [al for al in db.listar_alunos() if al.id in turma.id_alunos]
            alunos_com_nota = []
            
            for aluno in alunos:
                notas = db.listar_notas_por_aluno(aluno.id)
                nota_atual = next((n for n in notas if n.id_atividade == id_atividade), None)
                if nota_atual:
                    alunos_com_nota.append(f"{aluno.id} - {aluno.nome} (Nota atual: {nota_atual.nota})")
            
            if not alunos_com_nota:
                aluno_combo['values'] = ["Nenhum aluno com nota nesta atividade"]
            else:
                aluno_combo['values'] = alunos_com_nota
        
        ativ_combo.bind('<<ComboboxSelected>>', carregar_alunos_com_nota)
        
        def salvar_edicao():
            if not ativ_combo.get() or not aluno_combo.get() or not nota_entry.get():
                messagebox.showwarning("Campos vazios", "Preencha todos os campos!", parent=janela)
                return
            
            if "Nenhum aluno" in aluno_combo.get():
                messagebox.showwarning("Inválido", "Não há notas para editar.", parent=janela)
                return
            
            try:
                nota_valor = float(nota_entry.get())
            except ValueError:
                messagebox.showerror("Erro", "Nota inválida! Digite um número.", parent=janela)
                return
            
            id_atividade = ativ_combo.get().split(' - ')[0]
            id_aluno = aluno_combo.get().split(' - ')[0]
            
            nota = Nota(id_aluno=id_aluno, id_atividade=id_atividade, nota=nota_valor)
            db.salvar_ou_atualizar_nota(nota)
            
            messagebox.showinfo("Sucesso", "Nota atualizada com sucesso!", parent=janela)
            janela.destroy()
        
        tk.Button(frame, text="Atualizar Nota", bg=self.colors['warning'],
                 fg=self.colors['white'], font=('Segoe UI', 10, 'bold'),
                 relief='flat', cursor='hand2',
                 command=salvar_edicao).grid(row=3, column=0, columnspan=2, pady=20, ipadx=30, ipady=5)
    
    def visualizar_notas_professor(self):
        """Visualiza notas de alunos das turmas do professor - apenas suas turmas"""
        turmas = self.obter_turmas_professor()
        if not turmas:
            messagebox.showwarning("Sem turmas", "Você não tem turmas associadas.")
            return
        
        janela = tk.Toplevel(self.root)
        janela.title("Visualizar Notas de Aluno")
        janela.geometry("600x400")
        janela.resizable(False, False)
        janela.grab_set()
        
        frame_top = tk.Frame(janela, bg=self.colors['white'])
        frame_top.pack(fill='x', padx=20, pady=10)
        
        # Turma - apenas turmas do professor
        tk.Label(frame_top, text="Turma:", bg=self.colors['white'],
                font=('Segoe UI', 10)).grid(row=0, column=0, sticky='w', pady=5)
        turmas_opcoes = [f"{t.id} - {t.nome_disciplina}" for t in turmas]
        turma_combo = ttk.Combobox(frame_top, values=turmas_opcoes,
                                  font=('Segoe UI', 9), width=30, state='readonly')
        turma_combo.grid(row=0, column=1, pady=5)
        
        # Aluno
        tk.Label(frame_top, text="Aluno:", bg=self.colors['white'],
                font=('Segoe UI', 10)).grid(row=1, column=0, sticky='w', pady=5)
        aluno_combo = ttk.Combobox(frame_top, font=('Segoe UI', 9), width=30, state='readonly')
        aluno_combo.grid(row=1, column=1, pady=5)
        
        def atualizar_alunos(event):
            if not turma_combo.get():
                return
            id_turma = turma_combo.get().split(' - ')[0]
            turma = db.buscar_turma_por_id(id_turma)
            alunos = [al for al in db.listar_alunos(filter_ativos=False) if al.id in turma.id_alunos]
            alunos_opcoes = [f"{a.id} - {a.nome}" for a in alunos]
            aluno_combo['values'] = alunos_opcoes
        
        turma_combo.bind('<<ComboboxSelected>>', atualizar_alunos)
        
        # Text widget para exibir notas
        frame_text = tk.Frame(janela, bg=self.colors['white'])
        frame_text.pack(fill='both', expand=True, padx=20, pady=10)
        
        text_scroll = tk.Scrollbar(frame_text)
        text_scroll.pack(side='right', fill='y')
        
        notas_text = tk.Text(frame_text, font=('Consolas', 10),
                            yscrollcommand=text_scroll.set,
                            wrap='word', state='disabled')
        notas_text.pack(fill='both', expand=True)
        text_scroll.config(command=notas_text.yview)
        
        def buscar_notas():
            if not aluno_combo.get():
                messagebox.showwarning("Seleção vazia", "Selecione um aluno!", parent=janela)
                return
            
            id_aluno = aluno_combo.get().split(' - ')[0]
            aluno = db.buscar_aluno_por_id(id_aluno)
            notas = db.listar_notas_por_aluno(id_aluno)
            atividades = {atv.id: atv for atv in db.listar_atividades()}
            
            notas_text.config(state='normal')
            notas_text.delete('1.0', 'end')
            
            notas_text.insert('end', f"=== Notas de {aluno.nome} (RA: {aluno.ra}) ===\n\n")
            
            if not notas:
                notas_text.insert('end', "Nenhuma nota encontrada.\n")
            else:
                soma = 0
                for nota in notas:
                    ativ = atividades.get(nota.id_atividade)
                    desc = ativ.descricao if ativ else "Desconhecida"
                    notas_text.insert('end', f"• {desc}: {nota.nota}\n")
                    soma += nota.nota
                
                media = soma / len(notas)
                notas_text.insert('end', f"\n{'='*40}\n")
                notas_text.insert('end', f"Média: {media:.2f}\n")
            
            notas_text.config(state='disabled')
        
        tk.Button(frame_top, text="Buscar Notas", bg=self.colors['accent'],
                 fg=self.colors['white'], font=('Segoe UI', 10),
                 relief='flat', cursor='hand2',
                 command=buscar_notas).grid(row=2, column=0, columnspan=2, pady=10, ipadx=20, ipady=5)
    
    def criar_aba_chamadas_professor(self, parent):
        """Aba de chamadas do professor"""
        btn_frame = tk.Frame(parent, bg=self.colors['white'])
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(btn_frame, text="Registrar Chamada",
                 bg=self.colors['accent'], fg=self.colors['white'],
                 font=('Segoe UI', 10), relief='flat', cursor='hand2',
                 command=self.registrar_chamada_gui).pack(side='left', padx=5, ipady=5, ipadx=10)
        
        tk.Button(btn_frame, text="Editar Chamada",
                 bg=self.colors['warning'], fg=self.colors['white'],
                 font=('Segoe UI', 10), relief='flat', cursor='hand2',
                 command=self.editar_chamada_gui).pack(side='left', padx=5, ipady=5, ipadx=10)
        
        tk.Button(btn_frame, text="Visualizar Chamada",
                 bg=self.colors['accent'], fg=self.colors['white'],
                 font=('Segoe UI', 10), relief='flat', cursor='hand2',
                 command=self.visualizar_chamada_gui).pack(side='left', padx=5, ipady=5, ipadx=10)
        
        info_label = tk.Label(parent,
                             text="Selecione uma opção para gerenciar chamadas",
                             font=('Segoe UI', 12), bg=self.colors['white'],
                             fg=self.colors['secondary'])
        info_label.pack(expand=True)
    
    def mostrar_menu_aluno(self):
        """Exibe o menu principal do aluno com abas"""
        self.limpar_janela()
        self.criar_header(self.root)
        
        # Buscar dados do aluno
        aluno = db.buscar_aluno_por_id(self.usuario_id)
        if not aluno:
            messagebox.showerror("Erro", "Dados do aluno não encontrados!")
            self.fazer_logout()
            return
        
        main_frame = tk.Frame(self.root, bg=self.colors['light'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill='both', expand=True)
        
        # Aba 1: Minha Turma
        tab_turma = tk.Frame(notebook, bg=self.colors['white'])
        notebook.add(tab_turma, text='Minha Turma')
        self.criar_aba_turma_aluno(tab_turma, aluno)
        
        # Aba 2: Minhas Aulas
        tab_aulas = tk.Frame(notebook, bg=self.colors['white'])
        notebook.add(tab_aulas, text='Minhas Aulas')
        self.criar_aba_aulas_aluno(tab_aulas, aluno)
        
        # Aba 3: Minhas Atividades
        tab_atividades = tk.Frame(notebook, bg=self.colors['white'])
        notebook.add(tab_atividades, text='Minhas Atividades')
        self.criar_aba_atividades_aluno(tab_atividades, aluno)
        
        # Aba 4: Minhas Notas
        tab_notas = tk.Frame(notebook, bg=self.colors['white'])
        notebook.add(tab_notas, text='Minhas Notas')
        self.criar_aba_notas_aluno(tab_notas, aluno)
        
        # Aba 5: Minha Presença
        tab_presenca = tk.Frame(notebook, bg=self.colors['white'])
        notebook.add(tab_presenca, text='Minha Presença')
        self.criar_aba_presenca_aluno(tab_presenca, aluno)
    
    def criar_aba_turma_aluno(self, parent, aluno):
        """Mostra informações da turma do aluno"""
        info_frame = tk.Frame(parent, bg=self.colors['white'])
        info_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(info_frame, text="Informações da Minha Turma",
                font=('Segoe UI', 16, 'bold'), bg=self.colors['white'],
                fg=self.colors['primary']).pack(pady=20)
        
        if not aluno.id_turma:
            tk.Label(info_frame, text="Você não está matriculado em nenhuma turma.",
                    font=('Segoe UI', 12), bg=self.colors['white'],
                    fg=self.colors['danger']).pack(pady=50)
            return
        
        turma = db.buscar_turma_por_id(aluno.id_turma)
        if not turma:
            tk.Label(info_frame, text="Turma não encontrada.",
                    font=('Segoe UI', 12), bg=self.colors['white'],
                    fg=self.colors['danger']).pack(pady=50)
            return
        
        # Card com informações
        card_frame = tk.Frame(info_frame, bg=self.colors['light'],
                             relief='raised', borderwidth=2)
        card_frame.pack(pady=10, ipadx=20, ipady=20)
        
        tk.Label(card_frame, text=f"Turma: {turma.nome_disciplina}",
                font=('Segoe UI', 14, 'bold'), bg=self.colors['light']).pack(pady=5)
        
        tk.Label(card_frame, text=f"Seu RA: {aluno.ra}",
                font=('Segoe UI', 12), bg=self.colors['light']).pack(pady=5)
        
        tk.Label(card_frame, text=f"Total de alunos: {len(turma.id_alunos)}",
                font=('Segoe UI', 12), bg=self.colors['light']).pack(pady=5)
        
        # Lista de colegas
        tk.Label(info_frame, text="Colegas de Turma:",
                font=('Segoe UI', 12, 'bold'), bg=self.colors['white']).pack(pady=10)
        
        list_frame = tk.Frame(info_frame, bg=self.colors['white'])
        list_frame.pack(fill='both', expand=True, pady=10)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        colegas_listbox = tk.Listbox(list_frame, font=('Segoe UI', 10),
                                     yscrollcommand=scrollbar.set)
        colegas_listbox.pack(fill='both', expand=True)
        scrollbar.config(command=colegas_listbox.yview)
        
        todos_alunos = {al.id: al for al in db.listar_alunos()}
        for id_aluno in turma.id_alunos:
            if id_aluno != aluno.id and id_aluno in todos_alunos:
                colega = todos_alunos[id_aluno]
                colegas_listbox.insert('end', f"{colega.nome} (RA: {colega.ra})")
    
    def criar_aba_aulas_aluno(self, parent, aluno):
        """Mostra as aulas da turma do aluno"""
        if not aluno.id_turma:
            tk.Label(parent, text="Você não está matriculado em nenhuma turma.",
                    font=('Segoe UI', 12), bg=self.colors['white'],
                    fg=self.colors['danger']).pack(expand=True)
            return
        
        tk.Label(parent, text="Minhas Aulas", font=('Segoe UI', 14, 'bold'),
                bg=self.colors['white']).pack(pady=10)
        
        # Tabela de aulas
        table_frame = tk.Frame(parent, bg=self.colors['white'])
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(table_frame)
        scrollbar.pack(side='right', fill='y')
        
        aulas_tree = ttk.Treeview(table_frame,
                                 columns=('Data', 'Tópico', 'Professor'),
                                 show='headings',
                                 yscrollcommand=scrollbar.set)
        
        aulas_tree.heading('Data', text='Data')
        aulas_tree.heading('Tópico', text='Tópico')
        aulas_tree.heading('Professor', text='Professor')
        
        aulas_tree.column('Data', width=100)
        aulas_tree.column('Tópico', width=350)
        aulas_tree.column('Professor', width=200)
        
        scrollbar.config(command=aulas_tree.yview)
        aulas_tree.pack(fill='both', expand=True)
        
        # Carregar aulas
        aulas = [a for a in db.listar_aulas() if a.id_turma == aluno.id_turma]
        professores = {p.id: p.nome for p in db.listar_professores()}
        
        if not aulas:
            aulas_tree.insert('', 'end', values=('', 'Nenhuma aula registrada', ''))
        else:
            for aula in aulas:
                prof_nome = professores.get(aula.id_professor, "Desconhecido")
                aulas_tree.insert('', 'end', values=(aula.data, aula.topico, prof_nome))
    
    def criar_aba_atividades_aluno(self, parent, aluno):
        """Mostra as atividades da turma do aluno"""
        if not aluno.id_turma:
            tk.Label(parent, text="Você não está matriculado em nenhuma turma.",
                    font=('Segoe UI', 12), bg=self.colors['white'],
                    fg=self.colors['danger']).pack(expand=True)
            return
        
        tk.Label(parent, text="Minhas Atividades", font=('Segoe UI', 14, 'bold'),
                bg=self.colors['white']).pack(pady=10)
        
        # Lista de atividades
        list_frame = tk.Frame(parent, bg=self.colors['white'])
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        ativ_listbox = tk.Listbox(list_frame, font=('Segoe UI', 11),
                                 yscrollcommand=scrollbar.set)
        ativ_listbox.pack(fill='both', expand=True)
        scrollbar.config(command=ativ_listbox.yview)
        
        atividades = [a for a in db.listar_atividades() if a.id_turma == aluno.id_turma]
        
        if not atividades:
            ativ_listbox.insert('end', "Nenhuma atividade registrada para sua turma.")
        else:
            for i, ativ in enumerate(atividades, 1):
                ativ_listbox.insert('end', f"{i}. {ativ.descricao}")
    
    def criar_aba_notas_aluno(self, parent, aluno):
        """Mostra as notas do aluno"""
        tk.Label(parent, text="Minhas Notas", font=('Segoe UI', 14, 'bold'),
                bg=self.colors['white']).pack(pady=10)
        
        # Frame para mostrar notas
        info_frame = tk.Frame(parent, bg=self.colors['white'])
        info_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Text widget
        text_frame = tk.Frame(info_frame, bg=self.colors['white'])
        text_frame.pack(fill='both', expand=True)
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side='right', fill='y')
        
        notas_text = tk.Text(text_frame, font=('Consolas', 11),
                            yscrollcommand=scrollbar.set,
                            wrap='word', state='disabled',
                            bg=self.colors['light'])
        notas_text.pack(fill='both', expand=True)
        scrollbar.config(command=notas_text.yview)
        
        # Carregar notas
        notas = db.listar_notas_por_aluno(aluno.id)
        atividades = {atv.id: atv for atv in db.listar_atividades()}
        
        notas_text.config(state='normal')
        
        if not notas:
            notas_text.insert('end', "Você ainda não possui notas registradas.\n")
        else:
            notas_text.insert('end', f"{'='*50}\n")
            notas_text.insert('end', f"  BOLETIM DE {aluno.nome.upper()}\n")
            notas_text.insert('end', f"  RA: {aluno.ra}\n")
            notas_text.insert('end', f"{'='*50}\n\n")
            
            soma = 0
            for nota in notas:
                ativ = atividades.get(nota.id_atividade)
                desc = ativ.descricao if ativ else "Atividade Desconhecida"
                notas_text.insert('end', f"• {desc}\n")
                notas_text.insert('end', f"  Nota: {nota.nota}\n\n")
                soma += nota.nota
            
            media = soma / len(notas)
            notas_text.insert('end', f"{'='*50}\n")
            notas_text.insert('end', f"MÉDIA GERAL: {media:.2f}\n")
            notas_text.insert('end', f"{'='*50}\n")
        
        notas_text.config(state='disabled')
    
    def criar_aba_presenca_aluno(self, parent, aluno):
        """Mostra o histórico de presença do aluno"""
        tk.Label(parent, text="Meu Histórico de Presença",
                font=('Segoe UI', 14, 'bold'),
                bg=self.colors['white']).pack(pady=10)
        
        # Tabela de presença
        table_frame = tk.Frame(parent, bg=self.colors['white'])
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(table_frame)
        scrollbar.pack(side='right', fill='y')
        
        presenca_tree = ttk.Treeview(table_frame,
                                    columns=('Data', 'Tópico', 'Status'),
                                    show='headings',
                                    yscrollcommand=scrollbar.set)
        
        presenca_tree.heading('Data', text='Data')
        presenca_tree.heading('Tópico', text='Tópico da Aula')
        presenca_tree.heading('Status', text='Status')
        
        presenca_tree.column('Data', width=100)
        presenca_tree.column('Tópico', width=400)
        presenca_tree.column('Status', width=150)
        
        scrollbar.config(command=presenca_tree.yview)
        presenca_tree.pack(fill='both', expand=True)
        
        # Carregar chamadas
        chamadas = db.listar_chamadas_por_aluno(aluno.id)
        aulas = {aula.id: aula for aula in db.listar_aulas()}
        
        presencas = 0
        faltas = 0
        
        if not chamadas:
            presenca_tree.insert('', 'end', values=('', 'Nenhum registro de presença', ''))
        else:
            for chamada in chamadas:
                aula = aulas.get(chamada.id_aula)
                if aula:
                    status = "✓ Presente" if chamada.status == 'P' else "✗ Falta"
                    presenca_tree.insert('', 'end', values=(aula.data, aula.topico, status))
                    
                    if chamada.status == 'P':
                        presencas += 1
                    else:
                        faltas += 1
        
        # Estatísticas
        stats_frame = tk.Frame(parent, bg=self.colors['light'],
                              relief='raised', borderwidth=1)
        stats_frame.pack(fill='x', padx=10, pady=10, ipady=10)
        
        tk.Label(stats_frame, text=f"Presenças: {presencas}",
                font=('Segoe UI', 11, 'bold'), bg=self.colors['light'],
                fg=self.colors['success']).pack(side='left', padx=20)
        
        tk.Label(stats_frame, text=f"Faltas: {faltas}",
                font=('Segoe UI', 11, 'bold'), bg=self.colors['light'],
                fg=self.colors['danger']).pack(side='left', padx=20)
        
        if presencas + faltas > 0:
            percentual = (presencas / (presencas + faltas)) * 100
            tk.Label(stats_frame, text=f"Frequência: {percentual:.1f}%",
                    font=('Segoe UI', 11, 'bold'), bg=self.colors['light'],
                    fg=self.colors['primary']).pack(side='left', padx=20)


def main():
    """Função principal para iniciar a aplicação"""
    root = tk.Tk()
    app = AcademicSystemGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
