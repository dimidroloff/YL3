import sqlite3
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt6.uic import loadUi


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("main.ui", self)  # Загрузить интерфейс из main.ui

        # Настраиваем TableWidget
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels([
            "ID", "Название сорта", "Степень обжарки", "Формат", "Описание вкуса", "Цена", "Объем"
        ])
        self.load_data()

    def load_data(self):
        connection = sqlite3.connect("coffee.sqlite")
        cursor = connection.cursor()

        query = "SELECT * FROM coffee"
        rows = cursor.execute(query).fetchall()

        self.tableWidget.setRowCount(len(rows))

        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() ^ Qt.ItemFlag.ItemIsEditable)  # Запретить редактирование
                self.tableWidget.setItem(i, j, item)

        # Убираем вертикальный заголовок (счетчик строк)
        self.tableWidget.verticalHeader().setVisible(False)

        # Подгоняем ширину столбцов под содержимое
        self.tableWidget.resizeColumnsToContents()

        # Автоматическое растяжение последнего столбца
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        connection.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
