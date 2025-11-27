# src/modules/settings/settings_widget.py

from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QTimer
from pathlib import Path
from PyQt6.QtGui import QCursor
import pandas as pd

# Importa a função para salvar a configuração
from paths.config_path import save_config
# Importa o caminho atual (que agora é dinâmico)
from paths.dispensa.dispensa_path import DATA_DISPENSA_ELETRONICA_PATH
from modules.utils.coordinate_manager import CoordinateManager
from modules.utils.cc_manager import CCManager

class SettingsWidget(QWidget):
    """
    Este widget contém os botões para alterar os caminhos
    dos bancos de dados, configurações de automação e lista de CCs.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.coord_manager = CoordinateManager()
        self.cc_manager = CCManager()
        
        # Cria um ScrollArea para permitir rolar se a janela for pequena
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        
        # Widget de conteúdo dentro do scroll
        content_widget = QWidget()
        self.layout = QVBoxLayout(content_widget)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Define o widget de conteúdo no scroll
        scroll_area.setWidget(content_widget)
        
        # Layout principal deste widget (SettingsWidget)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # --- Título da Página ---
        self.title = QLabel("Configurações Gerais")
        self.title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px; color: #FFFFFF;")
        self.layout.addWidget(self.title)

        # --- 1. Seção do Banco de Dados ---
        self.setup_database_ui()

        # --- 2. Seção de Automação (Coordenadas) ---
        self.setup_automacao_ui()

        # --- 3. Seção de CC (Cópia) ---
        self.setup_cc_ui()
        
        self.layout.addStretch()

    def setup_database_ui(self):
        self.dispensa_group = QGroupBox("Banco de Dados (Dispensa Eletrônica)")
        self.dispensa_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        self.dispensa_layout = QVBoxLayout()

        self.dispensa_label = QLabel(f"Local atual:\n{DATA_DISPENSA_ELETRONICA_PATH}")
        self.dispensa_label.setWordWrap(True)
        
        self.dispensa_btn = QPushButton("Alterar Local do Banco (Dispensa)")
        self.dispensa_btn.clicked.connect(self.change_dispensa_db_path)
        
        self.dispensa_layout.addWidget(self.dispensa_label)
        self.dispensa_layout.addWidget(self.dispensa_btn)
        self.dispensa_group.setLayout(self.dispensa_layout)
        self.layout.addWidget(self.dispensa_group)

    def setup_automacao_ui(self):
        group = QGroupBox("Mapeamento de Coordenadas (Webmail)")
        group.setStyleSheet("QGroupBox { font-weight: bold; }")
        layout = QVBoxLayout()
        
        lbl_instr = QLabel("Clique em 'Capturar', posicione o mouse no local correto e aguarde 5 segundos.")
        lbl_instr.setStyleSheet("color: #CCC; font-style: italic;") # Cor clara para tema escuro
        layout.addWidget(lbl_instr)

        botoes_config = [
            ("1. Botão 'Novo Email'", "btn_novo_email"),
            ("2. Campo 'Para'", "campo_para"),
            ("3. Botão 'Exibir Cc' (Opcional)", "btn_exibir_cc"),
            ("4. Campo 'Cc'", "campo_cc"),
            ("5. Campo 'Assunto'", "campo_assunto"),
            ("6. Corpo do Email", "campo_corpo"),
            ("7. Botão 'Anexar' (Clipe)", "btn_anexar"),
            ("8. Botão 'Enviar'", "btn_enviar")
        ]

        for label_text, key in botoes_config:
            self.add_capture_row(layout, label_text, key)

        group.setLayout(layout)
        self.layout.addWidget(group)

    def setup_cc_ui(self):
        """Configura a seção de importação de lista de CCs."""
        self.cc_group = QGroupBox("Configuração de Destinatários em Cópia (CC)")
        self.cc_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        cc_layout = QVBoxLayout()

        # Botão de Importar
        self.btn_importar_cc = QPushButton("Importar Lista de CCs (Excel/CSV)")
        self.btn_importar_cc.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_importar_cc.clicked.connect(self.importar_ccs_planilha)
        cc_layout.addWidget(self.btn_importar_cc)

        cc_layout.addWidget(QLabel("E-mails salvos atualmente:"))

        # Lista visual
        self.lista_cc_widget = QListWidget()
        self.lista_cc_widget.setMaximumHeight(100)
        cc_layout.addWidget(self.lista_cc_widget)
        
        # Carrega a lista atual
        self.atualizar_lista_cc_visual()

        self.cc_group.setLayout(cc_layout)
        self.layout.addWidget(self.cc_group)

    # --- Métodos de Ação ---

    def change_dispensa_db_path(self):
        new_path, _ = QFileDialog.getSaveFileName(
            self, "Selecionar Banco de Dados", str(DATA_DISPENSA_ELETRONICA_PATH), "Database Files (*.db);;All Files (*)"
        )
        if new_path:
            new_path_obj = Path(new_path)
            save_config("DISPENSA_DB_PATH", str(new_path_obj))
            self.dispensa_label.setText(f"Local atual:\n{new_path_obj}")
            QMessageBox.information(self, "Configuração Salva", f"Local atualizado para:\n{new_path_obj}\nReinicie o app.")

    def add_capture_row(self, layout, label_text, key):
        row = QHBoxLayout()
        lbl = QLabel(label_text)
        lbl.setMinimumWidth(150)
        
        btn = QPushButton("Capturar (5s)")
        
        curr = self.coord_manager.get_coord(key)
        coords_text = f"X: {curr[0]}, Y: {curr[1]}" if curr else "Não definido"
        coords_lbl = QLabel(coords_text)
        coords_lbl.setMinimumWidth(100)
        
        btn.clicked.connect(lambda: self.start_capture(key, coords_lbl, btn))
        
        row.addWidget(lbl)
        row.addWidget(btn)
        row.addWidget(coords_lbl)
        layout.addLayout(row)

    def start_capture(self, key, label_widget, btn_widget):
        btn_widget.setText("Aguarde...")
        btn_widget.setEnabled(False)
        QTimer.singleShot(5000, lambda: self.save_cursor_pos(key, label_widget, btn_widget))

    def save_cursor_pos(self, key, label_widget, btn_widget):
        pos = QCursor.pos()
        self.coord_manager.save_coord(key, pos.x(), pos.y())
        label_widget.setText(f"X: {pos.x()}, Y: {pos.y()}")
        btn_widget.setText("Capturar (5s)")
        btn_widget.setEnabled(True)
        QApplication.beep()

    def atualizar_lista_cc_visual(self):
        self.lista_cc_widget.clear()
        emails = self.cc_manager.load_emails()
        if emails:
            self.lista_cc_widget.addItems(emails)
        else:
            self.lista_cc_widget.addItem("Nenhum e-mail de CC configurado.")

    def importar_ccs_planilha(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Selecionar Planilha", "", "Arquivos Excel/CSV (*.xlsx *.xls *.csv)")
        if not file_path: return

        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)
            
            lista_emails = df.iloc[:, 0].astype(str).tolist()
            self.cc_manager.save_emails(lista_emails)
            self.atualizar_lista_cc_visual()
            QMessageBox.information(self, "Sucesso", f"{len(lista_emails)} e-mails importados!")
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao ler arquivo:\n{str(e)}")
