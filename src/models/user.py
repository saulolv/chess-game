import sqlite3
import os

class User:
    def __init__ (self, db_file):
        self.db_file = db_file
        
        if not os.path.isfile(db_file):
            with sqlite3.connect(db_file) as conn:
                cursor = conn.cursor()
                cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, email TEXT, password TEXT)")
                conn.commit()
        
    def login(self, username, password):
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
                user = cursor.fetchone()
                
                if username == "" or password == "":
                    return "Preencha todos os campos!"
                
                if user:
                    return True
                else:
                    return False
        except sqlite3.Error as erro:
            print("Erro ao conectar no banco de dados!")
    
    def register(self, username, email, password, password2):
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
                existing_user = cursor.fetchone()
                cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
                existing_email = cursor.fetchone()
                
                if username == "" or email == "" or password == "" or password2 == "":
                    return "Preencha todos os campos!"
                elif existing_user:
                    return "o Username já está sendo usado!"
                elif existing_email:
                    return "Este email já está sendo usado, tente outro!"
                
                elif password != password2:
                    return "As senhas não coincidem!"
                else:
                    cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (username, email, password))
                    
                    conn.commit()
                    
                    return "Usuário cadastrado com sucesso!"
        except sqlite3.Error as erro:
            print("Erro ao conectar no banco de dados!")
            print(erro)
            return "Erro ao conectar no banco de dados!"
                
    def change_password(self, username, password):
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET password = ? WHERE username = ?", (password, username))
                conn.commit()
        except sqlite3.Error as erro:
            print("Erro ao conectar no banco de dados!")
            print(erro)
            return "Erro ao conectar no banco de dados!"
        
    def check_user(self, username, email):
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
                existing_user = cursor.fetchone()
                cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
                existing_email = cursor.fetchone()
                
                if username == "" or email == "":
                    return "Preencha todos os campos!"
                else:
                    if existing_user and existing_email:
                        return True
                    else:
                        return False
        except sqlite3.Error as erro:
            print("Erro ao conectar no banco de dados!")
            print(erro)
            return "Erro ao conectar no banco de dados!"