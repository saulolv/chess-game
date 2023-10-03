import pygame
from PyQt5 import uic, QtWidgets
from models.user import User
import random
from menus.send_email import send_email
import re
from game.startgame import main_game  

pygame.display.set_mode((1,1))

app = QtWidgets.QApplication([])

login_screen = uic.loadUi("src/assets/login_screen.ui")
register_screen = uic.loadUi("src/assets/register_screen.ui")
recover_screen = uic.loadUi("src/assets/recpass_screen.ui")
code_screen = uic.loadUi("src/assets/code_screen.ui")
newpass_screen = uic.loadUi("src/assets/chargepass_screen.ui")

user = User("src/assets/database.db")

def run_login(): 
    login_screen.pushButton.clicked.connect(login)
    login_screen.pushButton_2.clicked.connect(open_register_screen)
    register_screen.pushButton.clicked.connect(register)
    login_screen.pushButton_3.clicked.connect(open_recover_password_screen)
    recover_screen.pushButton.clicked.connect(recover_password)
    register_screen.pushButton_2.clicked.connect(open_login_screen)
    recover_screen.pushButton_2.clicked.connect(open_login_screen)
    code_screen.pushButton_2.clicked.connect(open_recover_password_screen)

    login_screen.show()
    app.exec()
    app.quit()

def open_login_screen():
    recover_screen.close()
    register_screen.close()
    login_screen.show()
    
def open_recover_password_screen():
    code_screen.close()
    login_screen.close()
    recover_screen.show()
    
def recover_password():
    recover_screen.label_3.setText("")
    username = recover_screen.lineEdit.text()
    email = recover_screen.lineEdit_2.text()
    
    result = user.check_user(username, email)
    
    if result == "Preencha todos os campos!":
        recover_screen.label_3.setText(result)
    elif result:
        recov_code = random.randint(100000, 999999)
        send_email(email, recov_code)
        codd = str(recov_code)
        code_screen.pushButton.clicked.connect(lambda: code(codd, username))
        recover_screen.close()
        code_screen.show()
    else:
        recover_screen.label_3.setText("Usuário ou email incorretos!")

    
def code(codd, username):
    code_screen.label_3.setText("")
    codet = code_screen.lineEdit.text()
    
    if codet == "":
        code_screen.label_3.setText("Preencha o campo!")
    
    elif codet == codd:
        code_screen.close()
        newpass_screen.show()
        newpass_screen.pushButton.clicked.connect(lambda: newpass(username))         
    else:
        code_screen.label_3.setText("Código incorreto!")
               
def newpass(username):
    newpass_screen.label_3.setText("")
    password = newpass_screen.lineEdit.text()
    password2 = newpass_screen.lineEdit_2.text()
    
    if password == "" or password2 == "":
        newpass_screen.label_3.setText("Preencha todos os campos!")
    elif password != password2:
        newpass_screen.label_3.setText("As senhas não coincidem!")
    else:
        user.change_password(username, password)
        newpass_screen.label_3.setText("Senha alterada com sucesso!")
        newpass_screen.close()
        login_screen.show()   
    
def login():
    login_screen.label_3.setText("")
    username = login_screen.lineEdit.text()
    password = login_screen.lineEdit_2.text()
    
    if username == "" or password == "":
        login_screen.label_3.setText("Preencha todos os campos!")
        return
    elif user.login(username, password):
        login_screen.label_3.setText("Login realizado com sucesso!")
        login_screen.close()
        main_game()
    else:
        login_screen.label_3.setText("Usuário ou senha incorretos!")

def open_register_screen():
    login_screen.close()
    register_screen.show()

def register():
    register_screen.label_5.setText("")
    register_screen.label_6.setText("")
    register_screen.label_7.setText("")
    register_screen.label_8.setText("")
    
    username = register_screen.lineEdit.text()
    email = register_screen.lineEdit_2.text()
    password = register_screen.lineEdit_3.text()
    password2 = register_screen.lineEdit_4.text()
    
    # Regex to check if the email is valid
    regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(regex, email):
        register_screen.label_7.setText("Email inválido!")
        return
    else:
        result = user.register(username, email, password, password2)
    
        if result == "Usuário cadastrado com sucesso!":
            register_screen.close()
            login_screen.show()
            login_screen.label_3.setText(result)
        else:
            error_labels = {
                "o Username já está sendo usado!": register_screen.label_6,
                "Este email já está sendo usado, tente outro!": register_screen.label_7,
                "Preencha todos os campos!": register_screen.label_5,
                "As senhas não coincidem!": register_screen.label_8,
            }
            error_label = error_labels[result]
            if error_label:
                error_label.setText(result)
    
            
    
    