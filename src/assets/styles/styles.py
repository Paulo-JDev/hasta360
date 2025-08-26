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

def get_full_dark_theme():
    """
    Retorna uma folha de estilos QSS completa para um tema escuro profissional.
    Baseado no popular QDarkStyleSheet.
    """
    return """
        QToolTip {
            color: #ffffff;
            background-color: #2a2a2a;
            border: 1px solid #323232;
            border-radius: 3px;
        }
        QWidget {
            color: #b1b1b1;
            background-color: #323232;
        }
        QTreeView, QListView {
            background-color: #2a2a2a;
        }
        QWidget:item:hover {
            background-color: #1e1e1e;
            color: #eff0f1;
        }
        QWidget:item:selected {
            background-color: #3d8ec9;
            color: #eff0f1;
        }
        QMenuBar::item {
            background: transparent;
        }
        QMenuBar::item:selected {
            background: transparent;
            border: 1px solid #3d8ec9;
        }
        QMenuBar::item:pressed {
            background: #444;
            border: 1px solid #000;
            background-color: QLinearGradient(
                x1:0, y1:0,
                x2:0, y2:1,
                stop:1 #3d8ec9,
                stop:0.4 #31363b
            );
            color: #b1b1b1;
        }
        QMenu {
            border: 1px solid #000;
        }
        QMenu::item {
            padding: 2px 20px 2px 20px;
        }
        QMenu::item:selected {
            color: #eff0f1;
        }
        QWidget:disabled {
            color: #454545;
            background-color: #323232;
        }
        QAbstractItemView {
            background-color: #2a2a2a;
            alternate-background-color: #323232;
            color: #eff0f1;
            border: 1px solid #323232;
        }
        QLineEdit, QSpinBox, QDoubleSpinBox, QTextEdit {
            background-color: #2a2a2a;
            padding: 5px;
            border-style: solid;
            border: 1px solid #3d8ec9;
            border-radius: 3px;
            color: #eff0f1;
        }
        QPushButton {
            color: #eff0f1;
            background-color: #484848;
            border-width: 1px;
            border-color: #1e1e1e;
            border-style: solid;
            border-radius: 6;
            padding: 8px;
            font-size: 14px;
            padding-left: 5px;
            padding-right: 5px;
        }
        QPushButton:hover {
            background-color: #585858;
        }
        QPushButton:pressed {
            background-color: #3d8ec9;
        }
        QComboBox {
            selection-background-color: #3d8ec9;
            background-color: #2a2a2a;
            border-style: solid;
            border: 1px solid #3d8ec9;
            border-radius: 3px;
        }
        QComboBox:hover, QPushButton:hover {
            border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #ca0619);
        }
        QComboBox:on {
            padding-top: 3px;
            padding-left: 4px;
            background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);
            selection-background-color: #3d8ec9;
        }
        QComboBox QAbstractItemView {
            border: 2px solid darkgray;
            selection-background-color: #3d8ec9;
        }
        QTableView {
            gridline-color: #646464;
        }
        QHeaderView::section {
            background-color: #323232;
            color: #eff0f1;
            padding: 5px;
            border: 1px solid #646464;
        }
        QProgressBar {
            border: 1px solid #646464;
            border-radius: 5px;
            text-align: center;
        }
        QProgressBar::chunk {
            background-color: #3d8ec9;
            width: 5px;
            margin: 0.5px;
        }
        QTabBar::tab {
            background: #323232;
            border: 1px solid #323232;
            border-bottom-left-radius: 0;
            border-bottom-right-radius: 0;
            padding: 10px;
        }
        QTabBar::tab:selected, QTabBar::tab:hover {
            background: #505050;
        }
        QTabWidget::pane {
            border: 1px solid #323232;
        }
        QGroupBox {
            border: 1px solid #3d8ec9;
            border-radius: 5px;
            margin-top: 1ex;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top center;
            padding: 0 3px;
        }
    """