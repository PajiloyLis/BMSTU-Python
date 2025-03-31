from view_model import MainWindow
from PyQt6.QtWidgets import QApplication

# Создание приложения и его окна
app = QApplication([])
window = MainWindow()
window.show()
app.exec()
