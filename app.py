# App design
# pip install pyqt6
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QComboBox, QDateEdit, QTableWidget, QVBoxLayout, QHBoxLayout, QMessageBox, QTableWidgetItem, QHeaderView

from PyQt6.QtCore import QDate, Qt
from database import fetch_expenses,add_expenses,delete_expenses

class ExpenseApp(QWidget):
    def __init__(self):
      super().__init__()
      self.initUI()
      self.load_table_data()
      self.setWindowTitle("Expense Tracker")

    #Design
    def initUI(self):
       #Create all objects
       self.date_box = QDateEdit()
       self.date_box.setDate(QDate.currentDate())
       self.dropdown = QComboBox()
       self.amount = QLineEdit()
       self.description = QLineEdit()

       self.btn_add = QPushButton("Add Expense")
       self.btn_delete = QPushButton("Delete Expense")
       self.btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
       self.btn_delete.setCursor(Qt.CursorShape.PointingHandCursor)

       self.table = QTableWidget(0, 5)
       self.table.setHorizontalHeaderLabels(["ID", "Date", "Category", "Amount", "Desription"])

       #edit table width
       self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

       self.add_dropdown() #dropdown menu

       self.btn_add.clicked.connect(self.add_expense)
       self.btn_delete.clicked.connect(self.delete_expenses)

       self.apply_styles()
       #Add Widgets to a Layout (Row/Column)
       self.setup_layout()

    def setup_layout(self):
       master = QVBoxLayout()
       row1 = QHBoxLayout()
       row2 = QHBoxLayout()
       row3 = QHBoxLayout()

       #Row 1
       row1.addWidget(QLabel("Date"))
       row1.addWidget(self.date_box)
       row1.addWidget(QLabel("Category"))
       row1.addWidget(self.dropdown)

       #Row 2
       row2.addWidget(QLabel("Amount"))
       row2.addWidget(self.amount)
       row2.addWidget(QLabel("Description"))
       row2.addWidget(self.description)

       #Row 3
       row3.addWidget(self.btn_add)
       row3.addWidget(self.btn_delete)

       master.addLayout(row1)
       master.addLayout(row2)
       master.addLayout(row3)
       master.addWidget(self.table)

       self.setLayout(master)

    def add_dropdown(self):
       categories = ["Food", "Rent", "Bills", "Entertainment", "Shopping", "Others"]
       self.dropdown.addItems(categories)

    def load_table_data(self):
       expenses = fetch_expenses()
       self.table.setRowCount(0)
       for row_idx, expense in enumerate(expenses):
          self.table.insertRow(row_idx)
          for col_idx, data in enumerate(expense):
             self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))

    def clear_inputs(self):
       self.date_box.setDate(QDate.currentDate())
       self.dropdown.setCurrentIndex(0)
       self.amount.clear()
       self.description.clear()

    def add_expense(self):
       date = self.date_box.date().toString("dd-MM-yyyy")
       category = self.dropdown.currentText() #QComboBox
       amount = self.amount.text() #QLineEdit
       description = self.description.text()

       if not amount or not description:
          QMessageBox.warning(self, "Input Error", "Amount and Description can not be empty")
          return
       
       if add_expenses(date, category, amount, description):
          self.load_table_data()
          self.clear_inputs()
       else:
         QMessageBox.critical(self, "Error", "Failed to add expense")

    def delete_expenses(self):
       selected_row = self.table.currentRow()
       if selected_row == -1:
          QMessageBox.warning(self, "Unknown", "Row is not selected to delete")
          return
       
       expense_id = int(self.table.item(selected_row, 0).text())
       confirm = QMessageBox.question(self, "Confirm", "Are you sure you want to delete?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

       if confirm == QMessageBox.StandardButton.Yes and delete_expenses(expense_id):
          self.load_table_data()

    def apply_styles(self):
       self.setStyleSheet("""
    QWidget {
        background-color: #1F1F28;
        font-family: 'Courier New', Courier, monospace;
        font-size: 15px;
        color: #DCD7BA;
    }

    QLabel {
        font-size: 17px;
        color: #E6C384;
        font-weight: bold;
        padding: 4px;
    }

    QLineEdit, QComboBox, QDateEdit {
        background-color: #16161D;
        font-size: 15px;
        color: #DCD7BA;
        border: 2px solid #7E9CD8;
        border-radius: 4px;
        padding: 6px;
        selection-background-color: #7E9CD8;
        selection-color: #1F1F28;
    }
    QLineEdit:hover, QComboBox:hover, QDateEdit:hover {
        border: 2px solid #E46876;
    }
    QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
        border: 2px solid #E46876;
        background-color: #223249;
    }

    QTableWidget {
        background-color: #16161D;
        alternate-background-color: #223249;
        gridline-color: #54546D;
        selection-background-color: #E6C384;
        selection-color: #1F1F28;
        font-size: 15px;
        border: 2px solid #7E9CD8;
    }
    QHeaderView::section {
        background-color: #7E9CD8;
        color: #1F1F28;
        font-weight: bold;
        padding: 4px;
        border: 2px solid #E6C384;
        font-family: 'Courier New', Courier, monospace;
        font-size: 15px;
    }

    QScrollBar:vertical {
        width: 14px;
        background-color: #1F1F28;
        border: 2px solid #7E9CD8;
    }
    QScrollBar::handle:vertical {
        background-color: #E6C384;
        min-height: 20px;
        border-radius: 4px;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        background: #7E9CD8;
        height: 0px;
    }

    QPushButton {
        background-color: #7E9CD8;
        color: #1F1F28;
        padding: 10px 18px;
        border: 2px solid #E6C384;
        border-radius: 4px;
        font-size: 15px;
        font-weight: bold;
        font-family: 'Courier New', Courier, monospace;
    }
    QPushButton:hover {
        background-color: #98BB6C;
        color: #1F1F28;
        border: 2px solid #FFA066;
    }
    QPushButton:pressed {
        background-color: #E46876;
        color: #DCD7BA;
        border: 2px solid #7E9CD8;
    }
    QPushButton:disabled {
        background-color: #54546D;
        color: #888;
        border: 2px solid #54546D;
    }

    QToolTip {
        background-color: #E6C384;
        color: #1F1F28;
        border: 2px solid #7E9CD8;
        font-size: 13px;
        padding: 5px;
        border-radius: 4px;
        font-family: 'Courier New', Courier, monospace;
    }
    """)