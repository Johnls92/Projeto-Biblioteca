import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, timedelta

def criar_banco_de_dados():
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS livros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        autor TEXT NOT NULL,
        disponibilidade INTEGER NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS emprestimos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL,
        livro_id INTEGER NOT NULL,
        data_emprestimo TEXT NOT NULL,
        data_devolucao TEXT NOT NULL,
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
        FOREIGN KEY(livro_id) REFERENCES livros(id)
    )
    ''')

    conn.commit()
    conn.close()

criar_banco_de_dados()

class BibliotecaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Biblioteca ECIT Cristiano Cartaxo")
        self.setup_ui()

    def setup_ui(self):
        self.tab_control = ttk.Notebook(self.root)

        self.tab_usuarios = ttk.Frame(self.tab_control)
        self.tab_livros = ttk.Frame(self.tab_control)
        self.tab_emprestimos = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab_usuarios, text='Usuários')
        self.tab_control.add(self.tab_livros, text='Livros')
        self.tab_control.add(self.tab_emprestimos, text='Empréstimos')

        self.tab_control.pack(expand=1, fill='both')

        self.setup_usuarios_tab()
        self.setup_livros_tab()
        self.setup_emprestimos_tab()

    def setup_usuarios_tab(self):
        ttk.Label(self.tab_usuarios, text="Nome:").grid(row=0, column=0, padx=10, pady=10)
        self.nome_entry = ttk.Entry(self.tab_usuarios)
        self.nome_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.tab_usuarios, text="Email:").grid(row=1, column=0, padx=10, pady=10)
        self.email_entry = ttk.Entry(self.tab_usuarios)
        self.email_entry.grid(row=1, column=1, padx=10, pady=10)

        self.adicionar_usuario_btn = ttk.Button(self.tab_usuarios, text="Adicionar Usuário", command=self.adicionar_usuario)
        self.adicionar_usuario_btn.grid(row=2, column=0, columnspan=2, pady=10)

        self.usuarios_tree = ttk.Treeview(self.tab_usuarios, columns=('ID', 'Nome', 'Email'), show='headings')
        self.usuarios_tree.heading('ID', text='ID')
        self.usuarios_tree.heading('Nome', text='Nome')
        self.usuarios_tree.heading('Email', text='Email')
        self.usuarios_tree.grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Label(self.tab_usuarios, text="Buscar Nome:").grid(row=4, column=0, padx=10, pady=10)
        self.buscar_nome_entry = ttk.Entry(self.tab_usuarios)
        self.buscar_nome_entry.grid(row=4, column=1, padx=10, pady=10)

        self.buscar_usuario_btn = ttk.Button(self.tab_usuarios, text="Buscar Usuário", command=self.buscar_usuario)
        self.buscar_usuario_btn.grid(row=5, column=0, columnspan=2, pady=10)

        self.editar_usuario_btn = ttk.Button(self.tab_usuarios, text="Editar Usuário", command=self.editar_usuario)
        self.editar_usuario_btn.grid(row=6, column=0, pady=10)

        self.apagar_usuario_btn = ttk.Button(self.tab_usuarios, text="Apagar Usuário", command=self.apagar_usuario)
        self.apagar_usuario_btn.grid(row=6, column=1, pady=10)

        self.atualizar_lista_usuarios()

    def adicionar_usuario(self):
        nome = self.nome_entry.get()
        email = self.email_entry.get()
        if nome and email:
            conn = sqlite3.connect('biblioteca.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuarios (nome, email) VALUES (?, ?)", (nome, email))
            conn.commit()
            conn.close()
            self.atualizar_lista_usuarios()
            self.nome_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")

    def atualizar_lista_usuarios(self):
        for row in self.usuarios_tree.get_children():
            self.usuarios_tree.delete(row)

        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, email FROM usuarios")
        usuarios = cursor.fetchall()
        conn.close()

        for usuario in usuarios:
            self.usuarios_tree.insert("", "end", values=(usuario[0], usuario[1], usuario[2]))

    def buscar_usuario(self):
        nome = self.buscar_nome_entry.get()
        for row in self.usuarios_tree.get_children():
            self.usuarios_tree.delete(row)

        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, email FROM usuarios WHERE nome LIKE ?", ('%' + nome + '%',))
        usuarios = cursor.fetchall()
        conn.close()

        for usuario in usuarios:
            self.usuarios_tree.insert("", "end", values=(usuario[0], usuario[1], usuario[2]))

    def editar_usuario(self):
        selected_item = self.usuarios_tree.selection()
        if not selected_item:
            messagebox.showwarning("Atenção", "Selecione um usuário para editar")
            return

        item = self.usuarios_tree.item(selected_item)
        usuario_id = item['values'][0]
        nome = self.nome_entry.get()
        email = self.email_entry.get()

        if nome and email:
            conn = sqlite3.connect('biblioteca.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE usuarios SET nome = ?, email = ? WHERE id = ?", (nome, email, usuario_id))
            conn.commit()
            conn.close()
            self.atualizar_lista_usuarios()
            self.nome_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")

    def apagar_usuario(self):
        selected_item = self.usuarios_tree.selection()
        if not selected_item:
            messagebox.showwarning("Atenção", "Selecione um usuário para apagar")
            return

        item = self.usuarios_tree.item(selected_item)
        usuario_id = item['values'][0]

        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
        conn.commit()
        conn.close()
        self.atualizar_lista_usuarios()

    def setup_livros_tab(self):
        ttk.Label(self.tab_livros, text="Título:").grid(row=0, column=0, padx=10, pady=10)
        self.titulo_entry = ttk.Entry(self.tab_livros)
        self.titulo_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.tab_livros, text="Autor:").grid(row=1, column=0, padx=10, pady=10)
        self.autor_entry = ttk.Entry(self.tab_livros)
        self.autor_entry.grid(row=1, column=1, padx=10, pady=10)

        self.adicionar_livro_btn = ttk.Button(self.tab_livros, text="Adicionar Livro", command=self.adicionar_livro)
        self.adicionar_livro_btn.grid(row=2, column=0, columnspan=2, pady=10)

        self.livros_tree = ttk.Treeview(self.tab_livros, columns=('ID', 'Título', 'Autor', 'Disponibilidade'), show='headings')
        self.livros_tree.heading('ID', text='ID')
        self.livros_tree.heading('Título', text='Título')
        self.livros_tree.heading('Autor', text='Autor')
        self.livros_tree.heading('Disponibilidade', text='Disponibilidade')
        self.livros_tree.grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Label(self.tab_livros, text="Buscar Título:").grid(row=4, column=0, padx=10, pady=10)
        self.buscar_titulo_entry = ttk.Entry(self.tab_livros)
        self.buscar_titulo_entry.grid(row=4, column=1, padx=10, pady=10)

        self.buscar_livro_btn = ttk.Button(self.tab_livros, text="Buscar Livro", command=self.buscar_livro)
        self.buscar_livro_btn.grid(row=5, column=0, columnspan=2, pady=10)

        self.editar_livro_btn = ttk.Button(self.tab_livros, text="Editar Livro", command=self.editar_livro)
        self.editar_livro_btn.grid(row=6, column=0, pady=10)

        self.apagar_livro_btn = ttk.Button(self.tab_livros, text="Apagar Livro", command=self.apagar_livro)
        self.apagar_livro_btn.grid(row=6, column=1, pady=10)

        self.atualizar_lista_livros()

    def adicionar_livro(self):
        titulo = self.titulo_entry.get()
        autor = self.autor_entry.get()
        if titulo and autor:
            conn = sqlite3.connect('biblioteca.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO livros (titulo, autor, disponibilidade) VALUES (?, ?, 1)", (titulo, autor))
            conn.commit()
            conn.close()
            self.atualizar_lista_livros()
            self.titulo_entry.delete(0, tk.END)
            self.autor_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")

    def atualizar_lista_livros(self):
        for row in self.livros_tree.get_children():
            self.livros_tree.delete(row)

        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, titulo, autor, disponibilidade FROM livros")
        livros = cursor.fetchall()
        conn.close()

        for livro in livros:
            disponibilidade = 'Disponível' if livro[3] == 1 else 'Indisponível'
            self.livros_tree.insert("", "end", values=(livro[0], livro[1], livro[2], disponibilidade))

    def buscar_livro(self):
        titulo = self.buscar_titulo_entry.get()
        for row in self.livros_tree.get_children():
            self.livros_tree.delete(row)

        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, titulo, autor, disponibilidade FROM livros WHERE titulo LIKE ?", ('%' + titulo + '%',))
        livros = cursor.fetchall()
        conn.close()

        for livro in livros:
            disponibilidade = 'Disponível' if livro[3] == 1 else 'Indisponível'
            self.livros_tree.insert("", "end", values=(livro[0], livro[1], livro[2], disponibilidade))

    def editar_livro(self):
        selected_item = self.livros_tree.selection()
        if not selected_item:
            messagebox.showwarning("Atenção", "Selecione um livro para editar")
            return

        item = self.livros_tree.item(selected_item)
        livro_id = item['values'][0]
        titulo = self.titulo_entry.get()
        autor = self.autor_entry.get()

        if titulo and autor:
            conn = sqlite3.connect('biblioteca.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE livros SET titulo = ?, autor = ? WHERE id = ?", (titulo, autor, livro_id))
            conn.commit()
            conn.close()
            self.atualizar_lista_livros()
            self.titulo_entry.delete(0, tk.END)
            self.autor_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")

    def apagar_livro(self):
        selected_item = self.livros_tree.selection()
        if not selected_item:
            messagebox.showwarning("Atenção", "Selecione um livro para apagar")
            return

        item = self.livros_tree.item(selected_item)
        livro_id = item['values'][0]

        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM livros WHERE id = ?", (livro_id,))
        conn.commit()
        conn.close()
        self.atualizar_lista_livros()

    def setup_emprestimos_tab(self):
        ttk.Label(self.tab_emprestimos, text="Usuário:").grid(row=0, column=0, padx=10, pady=10)
        self.usuario_combobox = ttk.Combobox(self.tab_emprestimos)
        self.usuario_combobox.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.tab_emprestimos, text="Livro:").grid(row=1, column=0, padx=10, pady=10)
        self.livro_combobox = ttk.Combobox(self.tab_emprestimos)
        self.livro_combobox.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(self.tab_emprestimos, text="Dias de Empréstimo:").grid(row=2, column=0, padx=10, pady=10)
        self.dias_entry = ttk.Entry(self.tab_emprestimos)
        self.dias_entry.grid(row=2, column=1, padx=10, pady=10)

        self.adicionar_emprestimo_btn = ttk.Button(self.tab_emprestimos, text="Adicionar Empréstimo", command=self.adicionar_emprestimo)
        self.adicionar_emprestimo_btn.grid(row=3, column=0, columnspan=2, pady=10)

        self.emprestimos_tree = ttk.Treeview(self.tab_emprestimos, columns=('ID', 'Usuário', 'Livro', 'Data Empréstimo', 'Data Devolução'), show='headings')
        self.emprestimos_tree.heading('ID', text='ID')
        self.emprestimos_tree.heading('Usuário', text='Usuário')
        self.emprestimos_tree.heading('Livro', text='Livro')
        self.emprestimos_tree.heading('Data Empréstimo', text='Data Empréstimo')
        self.emprestimos_tree.heading('Data Devolução', text='Data Devolução')
        self.emprestimos_tree.grid(row=4, column=0, columnspan=2, pady=10)

        self.excluir_emprestimo_btn = ttk.Button(self.tab_emprestimos, text="Excluir Empréstimo", command=self.excluir_emprestimo)
        self.excluir_emprestimo_btn.grid(row=5, column=0, columnspan=2, pady=10)

        self.atualizar_lista_emprestimos()
        self.atualizar_comboboxes()

    def adicionar_emprestimo(self):
        usuario = self.usuario_combobox.get()
        livro = self.livro_combobox.get()
        dias_emprestimo = self.dias_entry.get()
        if usuario and livro and dias_emprestimo.isdigit():
            dias_emprestimo = int(dias_emprestimo)
            data_emprestimo = datetime.now().strftime('%Y-%m-%d')
            data_devolucao = (datetime.now() + timedelta(days=dias_emprestimo)).strftime('%Y-%m-%d')

            conn = sqlite3.connect('biblioteca.db')
            cursor = conn.cursor()
            
            cursor.execute("SELECT id FROM usuarios WHERE nome = ?", (usuario,))
            usuario_id = cursor.fetchone()[0]
            
            cursor.execute("SELECT id FROM livros WHERE titulo = ?", (livro,))
            livro_id = cursor.fetchone()[0]

            cursor.execute("INSERT INTO emprestimos (usuario_id, livro_id, data_emprestimo, data_devolucao) VALUES (?, ?, ?, ?)",
                           (usuario_id, livro_id, data_emprestimo, data_devolucao))
            cursor.execute("UPDATE livros SET disponibilidade = 0 WHERE id = ?", (livro_id,))
            conn.commit()
            conn.close()

            self.atualizar_lista_emprestimos()
            self.atualizar_comboboxes()
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos corretamente!")

    def excluir_emprestimo(self):
        selected_item = self.emprestimos_tree.selection()
        if not selected_item:
            messagebox.showwarning("Atenção", "Selecione um empréstimo para excluir")
            return

        item = self.emprestimos_tree.item(selected_item)
        emprestimo_id = item['values'][0]
        livro_titulo = item['values'][2]

        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM emprestimos WHERE id = ?", (emprestimo_id,))
        
        cursor.execute("SELECT id FROM livros WHERE titulo = ?", (livro_titulo,))
        livro_id = cursor.fetchone()[0]
        cursor.execute("UPDATE livros SET disponibilidade = 1 WHERE id = ?", (livro_id,))
        
        conn.commit()
        conn.close()

        self.atualizar_lista_emprestimos()
        self.atualizar_comboboxes()

    def atualizar_lista_emprestimos(self):
        for row in self.emprestimos_tree.get_children():
            self.emprestimos_tree.delete(row)
        
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        cursor.execute("SELECT e.id, u.nome, l.titulo, e.data_emprestimo, e.data_devolucao FROM emprestimos e JOIN usuarios u ON e.usuario_id = u.id JOIN livros l ON e.livro_id = l.id")
        emprestimos = cursor.fetchall()
        conn.close()
        
        for emprestimo in emprestimos:
            self.emprestimos_tree.insert("", "end", values=(emprestimo[0], emprestimo[1], emprestimo[2], emprestimo[3], emprestimo[4]))

    def atualizar_comboboxes(self):
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT nome FROM usuarios")
        usuarios = cursor.fetchall()
        self.usuario_combobox['values'] = [usuario[0] for usuario in usuarios]
        
        cursor.execute("SELECT titulo FROM livros WHERE disponibilidade = 1")
        livros = cursor.fetchall()
        self.livro_combobox['values'] = [livro[0] for livro in livros]
        
        conn.close()

root = tk.Tk()
app = BibliotecaApp(root)
root.mainloop()
