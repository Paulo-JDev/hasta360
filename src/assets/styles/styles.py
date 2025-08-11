from PyQt6.QtGui import QIcon, QPixmap

def get_menu_button_style():
    return """
        QPushButton {
            background-color: transparent;
            font-weight: bold;
            font-size: 16px;
            text-align: left;
            border: 1px solid transparent;
            border-left: 2px solid transparent; 
            border-radius: 0px;
            padding: 5px;
            margin: 0px; 
        }
        QPushButton:hover {
            background-color: #181928;
            border-left: 2px solid transparent;
            color: white;
            border-radius: 0px;
            padding: 5px;
        }
    """

def get_menu_button_activated_style():
    return """
        QPushButton {
            background-color: #181928;
            color: white;
            font-weight: bold;
            font-size: 16px;
            text-align: left;
            border: 1px solid #181928;
            border-left: 2px solid #F3F3F3;
            border-radius: 0px;
            padding: 5px;
            margin: 0px; 
        }
    """

def get_menu_title_style():
    return """
        font-weight: bold;
        font-size: 22px;
        color: white;
        padding: 10px;
        margin: 0;
        background-color: transparent;
        border-bottom: 2px solid white;
    """

def get_content_title_style():
    return """
        QLabel {
            font-weight: bold;
            font-size: 22px;
            color: white;
            padding: 10px;
            margin: 0;
            background-color: rgba(0, 0, 0, 80);
            border-bottom: 1px solid white;
        }
    """

def get_transparent_title_style():
    return """
        QLabel {
            font-weight: bold;
            font-size: 22px;
            color: white;
            margin: 0;
            background-color: transparent;
            border: none;
        }
    """

def apply_table_custom_style(table_view):
    """
    Aplica um estilo CSS personalizado ao tableView.
    """
    table_view.setStyleSheet("""
        QTableView {
            font-size: 16px;
            background-color: #13141F;                      
        }
        QTableView::section {
            font-size: 16px;
            font-weight: bold; 
        }
        QHeaderView::section:horizontal {
            font-size: 16px;
            font-weight: bold;
        }
        QHeaderView::section:vertical {
            font-size: 16px;
        }
    """)

def get_dark_theme_input_style():
    """
    Retorna um estilo CSS completo para janelas de formulário em temas escuros,
    incluindo containers, labels e campos de entrada.
    """
    return """
        /* Define o fundo da própria janela/dialog como escuro */
        QDialog, QWidget {
            background-color: #1E1E1E;
        }

        /* Estilo para os containers (painéis que agrupam os campos) */
        QFrame, QGroupBox {
            background-color: #2C2F3F; /* Fundo do painel um pouco mais claro */
            border-radius: 6px;
        }

        /* Estilo para os títulos dos GroupBox */
        QGroupBox::title {
            color: #F0F0F0;
            font-weight: bold;
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 5px 10px;
        }

        /* Estilo para todos os textos (Labels) */
        QLabel {
            background-color: transparent; /* Garante que não tenham fundo próprio */
            color: #F0F0F0;               /* Cor do texto clara */
            font-size: 14px;
        }

        /* Estilo para os campos de entrada */
        QLineEdit, QTextEdit, QPlainTextEdit, QDateEdit, QComboBox {
            background-color: #1E1E1E; /* Fundo dos campos de texto */
            color: #F0F0F0;
            border: 1px solid #4E648B;
            border-radius: 5px;
            padding: 5px;
            font-size: 14px;
        }

        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QDateEdit:focus, QComboBox:focus {
            border: 1px solid #8AB4F7; /* Borda azul ao focar */
        }

        /* Estilos específicos para QComboBox */
        QComboBox::drop-down {
            border: none;
        }

        QComboBox QAbstractItemView {
            background-color: #2C2F3F;
            color: #F0F0F0;
            selection-background-color: #4E648B;
        }
    """