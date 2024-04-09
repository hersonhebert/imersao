import re
import csv
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QMessageBox
from PyQt5.uic import loadUi
import pandas as pd
import unidecode
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.sub_windows = ['p1.ui', 'p2.ui', 'p3.ui', 'p4.ui', 'p5.ui', 'p6.ui', 'result.ui']
        self.current_sub_window_index = 0
        self.text_name = ""
        self.text_cel = ""
        self.text_mail = ""

        # Leitura dos arquivos CSV
        self.r1 = pd.read_csv("p1.csv", sep=";")
        self.r2 = pd.read_csv("p2.csv", sep=";")
        self.r3 = pd.read_csv("p3.csv", sep=";")
        self.r4 = pd.read_csv("p4.csv", sep=";")
        self.r5 = pd.read_csv("p5.csv", sep=";")
        self.r6 = pd.read_csv("p6.csv", sep=";")
        self.jobs = pd.read_csv("soft_courses.csv", sep=";", encoding="ISO-8859-1")

        self.show_main_screen()

    def show_main_screen(self):
        self.main_window = loadUi('cadastro.ui')
        self.setCentralWidget(self.main_window)
        self.main_window.iniciar_game.clicked.connect(self.handle_iniciar_game_click)
        self.main_window.text_cel.setPlaceholderText("11999999999")
        self.main_window.text_mail.setPlaceholderText("example@example.com")

    def handle_iniciar_game_click(self):
        self.text_name = self.main_window.text_name.toPlainText()
        self.text_cel = self.main_window.text_cel.toPlainText()
        self.text_mail = self.main_window.text_mail.toPlainText()

        if not self.text_name:
            QMessageBox.critical(self, "Erro", "Por favor, insira seu nome.")
            return

        if not self.validar_celular(self.text_cel):
            QMessageBox.critical(self, "Erro", "Número de celular inválido.")
            return
        
        if not self.validar_email(self.text_mail):
            QMessageBox.critical(self, "Erro", "E-mail inválido.")
            return

        print(self.text_name)
        print(self.text_cel)
        print(self.text_mail)

        self.save_to_csv()
        self.show_next_sub_screen()

    def save_to_csv(self):
        with open('dados_usuario.csv', 'a', newline='') as csvfile:
            fieldnames = ['Nome', 'Celular', 'Email']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow({'Nome': self.text_name, 'Celular': self.text_cel, 'Email': self.text_mail})

    def show_next_sub_screen(self):
        if self.current_sub_window_index < len(self.sub_windows):
            ui_file = self.sub_windows[self.current_sub_window_index]
            self.show_sub_screen(ui_file)
            self.current_sub_window_index += 1

    def show_sub_screen(self, ui_file):
        self.sub_window = loadUi(ui_file)
        self.connect_buttons()  
        self.setCentralWidget(self.sub_window)

    def connect_buttons(self):
        for button in self.sub_window.findChildren(QPushButton):
            button.clicked.connect(self.show_next_sub_screen)
            button.clicked.connect(self.handle_button_click)

    def handle_button_click(self):
        clicked_button = self.sender()
        if clicked_button:
            button_text = clicked_button.text()

            if self.current_sub_window_index == 2:
                self.r1 = self.r1[self.r1['A'] == unidecode.unidecode(button_text.lower())]
            elif self.current_sub_window_index == 3:
                self.r2 = self.r2[self.r2['A'] == unidecode.unidecode(button_text.lower())]
            elif self.current_sub_window_index == 4:
                self.r3 = self.r3[self.r3['A'] == unidecode.unidecode(button_text.lower())]
            elif self.current_sub_window_index == 5:
                self.r4 = self.r4[self.r4['A'] == unidecode.unidecode(button_text.lower())]
            elif self.current_sub_window_index == 6:
                if unidecode.unidecode(button_text.lower()) == "nao tomar banho":
                    self.r5 = self.r5[self.r5['A'] == 1]
                else:
                    self.r5 = self.r5[self.r5['A'] == 2]
            elif self.current_sub_window_index == 7:
                if unidecode.unidecode(button_text.lower()) == "nunca mais usar sapatos":
                    self.r6 = self.r6[self.r6['A'] == 2]
                else:
                    self.r6 = self.r6[self.r6['A'] == 1]

                self.determine_soft_skills()

    def determine_soft_skills(self):
        answer_skills = list(set(self.r1["B"]) | set(self.r2["B"]) | set(self.r3["B"]) | set(self.r4["B"]) | (set(self.r5["B"]) & set(self.r6["B"])))
        
        self.jobs['Soft Skills'] = self.jobs["Soft Skills"].apply(lambda x: x.split(','))
        self.jobs['Contagem'] = self.jobs['Soft Skills'].apply(lambda skills: sum(skill in answer_skills for skill in skills))
        max_contagem = self.jobs["Contagem"].max()
        
        selection = self.jobs["Profissoes do Futuro"][self.jobs["Contagem"] == max_contagem]
        selection = selection.to_list()

        # Exibindo o resultado no QLabel da result.ui
        self.show_result(selection)

    def show_result(self, selection):
        # Carregar a interface do arquivo result.ui
        result_window = loadUi('result.ui')

        # Acessar o QLabel com o nome result_label
        result_label_title = result_window.findChild(QLabel, 'result_label_title')
        result_label_corpo = result_window.findChild(QLabel, 'result_label_corpo')
        string_label = ""
        if(len(selection)>1):
            string_label = "As Profissões do Futuro para Você:\n"
        else:
            string_label = "A Profissão do Futuro para Você:\n"

        # Atualizar o texto do QLabel com o resultado
        result_label_title.setText(string_label.upper() + '\n')
        result_label_corpo.setText('\n'.join(selection).upper())

        # Exibir a janela result.ui
        self.setCentralWidget(result_window)

    def validar_celular(self, celular):
        # Verifica se o número de celular contém apenas dígitos e tem exatamente 11 caracteres
        return re.match(r'^\d{11}$', celular)

    def validar_email(self, email):
        # Usa uma expressão regular para validar o formato do e-mail
        return re.match(r'^[\w\.-]+@[\w\.-]+(\.[\w]+)+$', email)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.showMaximized()  
    sys.exit(app.exec_())
