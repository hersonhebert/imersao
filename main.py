import re
import csv
import pandas as pd
import unidecode
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
import photo
import fundo


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.sub_windows = ['p1.ui', 'p2.ui', 'p3.ui', 'p4.ui', 'p5.ui', 'p6.ui', 'result.ui']
        self.current_sub_window_index = 0
        self.text_name = ""
        self.text_cel = ""
        self.text_mail = ""
        self.data_frames = []
        self.jobs = pd.DataFrame()

        self.show_main_screen()

    def show_main_screen(self):
        self.setWindowTitle("Imersão na Educação do Futuro")
        self.setWindowIcon(QIcon('senai.ico'))
        self.main_window = loadUi('cadastro.ui')
        self.setCentralWidget(self.main_window)
        self.main_window.iniciar_game.clicked.connect(self.handle_iniciar_game_click)
        self.main_window.text_name.setMaxLength(40)
        self.main_window.text_cel.setPlaceholderText("11999999999")
        self.main_window.text_cel.setMaxLength(11)
        self.main_window.text_mail.setPlaceholderText("example@example.com")
        self.main_window.text_mail.setMaxLength(40)

    def handle_iniciar_game_click(self):
        self.text_name = self.main_window.text_name.text()
        self.text_cel = self.main_window.text_cel.text()
        self.text_mail = self.main_window.text_mail.text()

        if not self.text_name:
            QMessageBox.critical(self, "Erro", "Por favor, insira seu nome.")
            return

        if not re.match(r'^\d{11}$', self.text_cel):
            QMessageBox.critical(self, "Erro", "Número de celular inválido.")
            return
        
        if not re.match(r'^[\w\.-]+@[\w\.-]+(\.[\w]+)+$', self.text_mail):
            QMessageBox.critical(self, "Erro", "E-mail inválido.")
            return

        self.load_data_frames()
        self.save_to_csv()
        self.show_next_sub_screen()

    def load_data_frames(self):
        self.data_frames = [pd.read_csv(f"p{i}.csv", sep=";") for i in range(1, 7)]
        self.jobs = pd.read_csv("soft_courses.csv", sep=";")

    def save_to_csv(self):
        photo_path = "photos/photo_"+unidecode.unidecode(self.text_name)+"_"+self.text_cel+".jpg"
        with open('dados_usuario.csv', 'a', newline='', encoding = 'utf-8') as csvfile:
            fieldnames = ['Nome', 'Celular', 'Email', 'Foto']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow({'Nome': self.text_name, 'Celular': self.text_cel, 'Email': self.text_mail, 'Foto':photo_path})

    def show_next_sub_screen(self):
        if self.current_sub_window_index < len(self.sub_windows):
            ui_file = self.sub_windows[self.current_sub_window_index]
            self.show_sub_screen(ui_file)
            self.current_sub_window_index += 1

    def show_sub_screen(self, ui_file):
        sub_window = loadUi(ui_file)
        self.connect_buttons(sub_window)  
        self.setCentralWidget(sub_window)

    def connect_buttons(self, sub_window):
        for button in sub_window.findChildren(QPushButton):
            button.clicked.connect(self.show_next_sub_screen)
            button.clicked.connect(self.handle_button_click)

    def handle_button_click(self):
        clicked_button = self.sender()
        if clicked_button:
            button_text = clicked_button.text()
            current_frame = self.data_frames[self.current_sub_window_index - 2]
            self.filter_data_frame(current_frame, button_text)

    def filter_data_frame(self, data_frame, button_text):
        if self.current_sub_window_index == 2:
            self.r1 = data_frame[data_frame['A'] == unidecode.unidecode(button_text.lower())]
        elif self.current_sub_window_index == 3:
            self.r2 = data_frame[data_frame['A'] == unidecode.unidecode(button_text.lower())]
        elif self.current_sub_window_index == 4:
            self.r3 = data_frame[data_frame['A'] == unidecode.unidecode(button_text.lower())]
        elif self.current_sub_window_index == 5:
            self.r4 = data_frame[data_frame['A'] == unidecode.unidecode(button_text.lower())]
        elif self.current_sub_window_index == 6:
            if unidecode.unidecode(button_text.lower()) == "nao tomar banho":
                self.r5 = data_frame[data_frame['A'] == 1]
            else:
                self.r5 = data_frame[data_frame['A'] == 2]
        elif self.current_sub_window_index == 7:
            if unidecode.unidecode(button_text.lower()) == "nunca mais usar sapatos":
                self.r6 = data_frame[data_frame['A'] == 2]
            else:
                self.r6 = data_frame[data_frame['A'] == 1]

            self.determine_soft_skills()

    def determine_soft_skills(self):
        answer_skills = list(set(self.r1["B"]) | set(self.r2["B"]) | set(self.r3["B"]) | set(self.r4["B"]) | (set(self.r5["B"]) & set(self.r6["B"])))
        
        if not isinstance(self.jobs['Soft Skills'].iloc[0], list):
            self.jobs['Soft Skills'] = self.jobs["Soft Skills"].apply(lambda x: x.split(','))

        self.jobs['Contagem'] = self.jobs['Soft Skills'].apply(lambda skills: sum(skill in answer_skills for skill in skills))
        max_contagem = self.jobs["Contagem"].max()
        
        selection = self.jobs["Profissoes do Futuro"][self.jobs["Contagem"] == max_contagem]
        selection = selection.to_list()
        photo.main()
        fundo.image_fundo(self.text_name, self.text_cel)
        self.show_result(selection)

    def show_result(self, selection):
        result_window = loadUi('result.ui')
        result_label_title = result_window.findChild(QLabel, 'result_label_title')
        result_label_corpo = result_window.findChild(QLabel, 'result_label_corpo')
        result_label_foto = result_window.findChild(QLabel, 'photo_label')
        string_label = "As Profissões do Futuro para Você:\n" if len(selection) > 1 else "A Profissão do Futuro para Você:\n"

        result_label_title.setText(string_label.upper() + '\n')
        result_label_corpo.setText('\n'.join(selection).upper())
        string_photo = "photos/photo_"+unidecode.unidecode(self.text_name)+"_"+self.text_cel+".jpg"
        pixmap = QPixmap(string_photo)
        result_label_foto.setPixmap(pixmap)

        result_window.findChild(QPushButton, 'reset_button').clicked.connect(self.reset_application)
        self.setCentralWidget(result_window)

    def reset_application(self):
        self.current_sub_window_index = 0
        self.show_main_screen()
        self.showFullScreen()
        QApplication.instance().processEvents()
        self.update()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.showFullScreen()  
    sys.exit(app.exec_())
