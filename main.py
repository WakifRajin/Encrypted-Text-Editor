from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QFileDialog, QInputDialog, QMessageBox, QPushButton, QLineEdit
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from encryptor import encrypt_message, decrypt_message
import sys, os

class EncryptedTextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Encrypted Text Editor")
        self.setGeometry(300, 100, 800, 600)
        self.file_path = None
        self.init_ui()

    def init_ui(self):
        # Load stylesheet
        with open("futuristic.qss", "r") as f:
            self.setStyleSheet(f.read())

        # Central Widget
        self.text_area = QTextEdit(self)
        self.text_area.setPlaceholderText("Start typing...")

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_file)

        open_button = QPushButton("Open")
        open_button.clicked.connect(self.open_file)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.text_area)
        layout.addWidget(save_button)
        layout.addWidget(open_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Encrypted Files (*.awraxin)")
        if file_path:
            password, ok = QInputDialog.getText(self, "Password", "Enter password to open file:", echo=QInputDialog.EchoMode.Password)
            if ok and password:
                try:
                    with open(file_path, "rb") as file:
                        salt = file.read(16)
                        encrypted_data = file.read()
                        decrypted_data = decrypt_message(encrypted_data, password, salt)
                        self.text_area.setText(decrypted_data)
                        self.file_path = file_path
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to open file: {str(e)}")

    def save_file(self):
        if not self.file_path:
            self.file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Encrypted Files (*.awraxin)")
        if self.file_path:
            password, ok = QInputDialog.getText(self, "Password", "Enter password to save file:", echo=QLineEdit.EchoMode.Password)
            if ok and password:
                try:
                    text = self.text_area.toPlainText()
                    salt, encrypted_data = encrypt_message(text, password)
                    with open(self.file_path, "wb") as file:
                        file.write(salt)
                        file.write(encrypted_data)
                    QMessageBox.information(self, "Success", "File saved successfully!")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to save file: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = EncryptedTextEditor()
    
    icon_path = "appicon.ico"
    if os.path.exists(icon_path):
        editor.setWindowIcon(QIcon(icon_path))
    else:
        print("Warning: Icon file not found. Please check the path!")

    editor.show()
    sys.exit(app.exec())
