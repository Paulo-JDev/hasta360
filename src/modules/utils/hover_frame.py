from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import QEvent, pyqtSignal # 1. Importa o pyqtSignal

class HoverFrame(QFrame):
    """
    Um QFrame customizado que muda seu estilo com o hover
    e emite um sinal de clique.
    """
    # 2. Cria um novo sinal que podemos usar, chamado 'clicked'
    clicked = pyqtSignal()

    def __init__(self, normal_style, hover_style, parent=None):
        super().__init__(parent)
        self.normal_style = normal_style
        self.hover_style = hover_style
        self.setStyleSheet(self.normal_style)

    # 3. Adiciona o método que lida com o clique do mouse
    def mousePressEvent(self, event: QEvent):
        """Chamado quando o mouse é pressionado sobre o widget."""
        self.clicked.emit() # Emite nosso sinal personalizado
        super().mousePressEvent(event)

    def enterEvent(self, event: QEvent):
        """Chamado quando o mouse entra no widget."""
        self.setStyleSheet(self.hover_style)
        super().enterEvent(event)

    def leaveEvent(self, event: QEvent):
        """Chamado quando o mouse sai do widget."""
        self.setStyleSheet(self.normal_style)
        super().leaveEvent(event)