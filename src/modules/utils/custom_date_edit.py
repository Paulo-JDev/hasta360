from PyQt6.QtWidgets import QDateEdit, QCalendarWidget
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import QDate

class CustomDateEdit(QDateEdit):
    def __init__(self, icons, parent=None):
        super().__init__(parent)
        
        # Configura o popup do calendário
        self.setCalendarPopup(True)
        calendar = QCalendarWidget()
        
        # Define o tamanho fixo do QCalendarWidget para aumentar a área de visualização
        calendar.setFixedSize(400, 300)  # Definindo a largura para 400px e a altura para 300px
        self.setCalendarWidget(calendar)
        
        self.setDate(QDate.currentDate())