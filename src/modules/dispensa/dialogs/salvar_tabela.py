from PyQt6.QtWidgets import *
from modules.dispensa.dialogs.gerar_tabela import TabelaResumidaManager
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import QSize
class DataManager(QDialog):
    def __init__(self, icons, model, controller, parent=None):
        super().__init__(parent)
        self.icons = icons
        self.model = model
        self.controller = controller  # Referência ao controlador

        self.setWindowTitle("Database")
        self.setWindowIcon(self.icons["data-server"])
        self.setFixedSize(300, 300)
        layout = QVBoxLayout()
        self.setStyleSheet("QWidget { font-size: 16px; }")

        # Layout e configuração dos botões
        title_layout = QHBoxLayout()
        title_label = QLabel("Gerenciamento\nde Dados")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        title_layout.addWidget(title_label)
        layout.addLayout(title_layout)

        # Botão para salvar tabela completa
        btn_tabela_completa = QPushButton(" Tabela Completa", self)
        btn_tabela_completa.setIcon(self.icons["table"])
        btn_tabela_completa.setIconSize(QSize(40, 40))
        btn_tabela_completa.clicked.connect(self.controller.salvar_tabela_completa)
        layout.addWidget(btn_tabela_completa)

        # Botão para salvar tabela resumida
        btn_tabela_resumida = QPushButton(" Tabela Resumida", self)
        btn_tabela_resumida.setIcon(self.icons["table"])
        btn_tabela_resumida.setIconSize(QSize(40, 40))
        btn_tabela_resumida.clicked.connect(self.controller.salvar_tabela_resumida)
        layout.addWidget(btn_tabela_resumida)

        # Botão para carregar tabela
        btn_carregar_tabela = QPushButton(" Carregar Tabela", self)
        btn_carregar_tabela.setIcon(self.icons["loading_table"])
        btn_carregar_tabela.setIconSize(QSize(40, 40))
        btn_carregar_tabela.clicked.connect(self.controller.carregar_tabela)
        layout.addWidget(btn_carregar_tabela)

        # Botão para excluir a tabela 'controle_dispensas'
        btn_excluir_database = QPushButton(" Excluir Database", self)
        btn_excluir_database.setIcon(self.icons["delete"])
        btn_excluir_database.setIconSize(QSize(40, 40))
        btn_excluir_database.clicked.connect(self.controller.excluir_database)
        layout.addWidget(btn_excluir_database)

        self.setLayout(layout)