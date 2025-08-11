from PyQt6.QtWidgets import QWidget

def apply_internal_widget_styles(widget: QWidget):
    """Applies styles to ensure internal widgets have a white background."""
    widget.setStyleSheet("""
        QGroupBox, QLabel, QLineEdit, QTextEdit, QComboBox, QDateEdit, QListView, QTableView {
            background-color: white;
            border: 1px solid #C0C0C0;
            font-size: 14px;
        }

        QLineEdit, QTextEdit {
            padding: 4px;
            border-radius: 4px;
        }

        QTableView {
            gridline-color: #C0C0C0;
        }

        QComboBox::drop-down {
            border: none;
        }

        QGroupBox {
            border: 2px solid #C0C0C0;
            border-radius: 5px;
            margin-top: 10px;
            font-weight: bold;
        }
    """)
