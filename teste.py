import sys
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer

class CameraWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.camera = cv2.VideoCapture(0)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.capture_button = QPushButton("Capture", self)
        self.capture_button.clicked.connect(self.capture_image)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.capture_button)

        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.display_frame)
        self.timer.start(1000 // 30)  # Atualiza a tela a cada 30 milissegundos

    def display_frame(self):
        ret, frame = self.camera.read()
        if ret:
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            self.image_label.setPixmap(pixmap)

    def capture_image(self):
        ret, frame = self.camera.read()
        if ret:
            cv2.imwrite("captured_image.jpg", frame)
            print("Image captured and saved as 'captured_image.jpg'.")

    def closeEvent(self, event):
        self.camera.release()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = CameraWidget()
    widget.show()
    sys.exit(app.exec_())
