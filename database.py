import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QComboBox

class TaskManager(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

        self.conn = sqlite3.connect("tasks.db")
        self.cursor = self.conn.cursor()
        self.create_table()

    def initUI(self):
        self.setWindowTitle("Управление задачами")

        layout = QVBoxLayout()

        self.task_input = QTextEdit(self)
        layout.addWidget(QLabel("Введите задачу:"))
        layout.addWidget(self.task_input)

        self.difficulty_input = QComboBox(self)
        self.difficulty_input.addItems(["Легкий", "Средний", "Сложный"])
        layout.addWidget(QLabel("Выберите уровень сложности:"))
        layout.addWidget(self.difficulty_input)

        self.add_task_button = QPushButton("Добавить задачу", self)
        self.add_task_button.clicked.connect(self.add_task)
        layout.addWidget(self.add_task_button)

        self.generate_task_button = QPushButton("Составить вариант задания", self)
        self.generate_task_button.clicked.connect(self.generate_task)
        layout.addWidget(self.generate_task_button)

        self.output = QTextEdit(self)
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        self.setLayout(layout)

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            task TEXT,
                            difficulty TEXT
                        )''')
        self.conn.commit()

    def add_task(self):
        task = self.task_input.toPlainText()
        difficulty = self.difficulty_input.currentText()

        if task:
            self.cursor.execute("INSERT INTO tasks (task, difficulty) VALUES (?, ?)", (task, difficulty))
            self.conn.commit()
            self.output.append("Задача добавлена!")
        else:
            self.output.append("Задача не может быть пустой!")

    def generate_task(self):
        difficulty = self.difficulty_input.currentText()
        self.cursor.execute("SELECT task FROM tasks WHERE difficulty=?", (difficulty,))
        tasks = self.cursor.fetchall()

        if tasks:
            self.output.append(f"Составленный вариант задания ({difficulty}):")
            for task in tasks:
                self.output.append(task[0])
        else:
            self.output.append("Нет задач с выбранным уровнем сложности.")

if __name__ == "__main__":
    app = QApplication([])
    window = TaskManager()
    window.show()
    app.exec_()
