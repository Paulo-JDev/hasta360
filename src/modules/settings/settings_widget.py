from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from pathlib import Path
# Importa a função para salvar a configuração
from paths.config_path import save_config
# Importa o caminho atual (que agora é dinâmico)
from paths.dispensa.dispensa_path import DATA_DISPENSA_ELETRONICA_PATH

class SettingsWidget(QWidget):
    """
    Este widget contém os botões para alterar os caminhos
    dos bancos de dados e outras configurações.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Título da Página
        self.title = QLabel("Configurações Gerais")
        self.title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px; color: #FFFFFF;") # Adicionado Cor
        self.layout.addWidget(self.title)

        # --- Seção do Banco de Dados da Dispensa ---
        self.dispensa_group = QGroupBox("Banco de Dados (Dispensa Eletrônica)")
        self.dispensa_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        self.dispensa_layout = QVBoxLayout()

        # Label para mostrar o caminho atual
        self.dispensa_label = QLabel(f"Local atual:\n{DATA_DISPENSA_ELETRONICA_PATH}")
        self.dispensa_label.setWordWrap(True) # Quebra de linha
        
        # Botão para alterar o caminho
        self.dispensa_btn = QPushButton("Alterar Local do Banco (Dispensa)")
        self.dispensa_btn.clicked.connect(self.change_dispensa_db_path)
        
        self.dispensa_layout.addWidget(self.dispensa_label)
        self.dispensa_layout.addWidget(self.dispensa_btn)
        self.dispensa_group.setLayout(self.dispensa_layout)
        
        self.layout.addWidget(self.dispensa_group)
        
        # (Adicione outros QGroupBox aqui para outros bancos de dados no futuro)

        self.layout.addStretch() # Empurra tudo para o topo


    def change_dispensa_db_path(self):
        """
        Abre um QFileDialog para o usuário selecionar um arquivo .db
        e salva a escolha no config.json.
        """
        new_path, _ = QFileDialog.getSaveFileName(
            self,
            "Selecionar Banco de Dados da Dispensa",
            str(DATA_DISPENSA_ELETRONICA_PATH), # Começa no local atual
            "Database Files (*.db);;All Files (*)"
        )
        
        if new_path:
            new_path_obj = Path(new_path)
            
            # Salva o novo caminho no config.json
            save_config("DISPENSA_DB_PATH", str(new_path_obj))
            
            # Atualiza o label na tela
            self.dispensa_label.setText(f"Local atual:\n{new_path_obj}")
            
            # Informa o usuário que precisa reiniciar
            QMessageBox.information(
                self, 
                "Configuração Salva",
                f"O local do banco de dados foi atualizado para:\n{new_path_obj}\n\n"
                "Por favor, reinicie o aplicativo para que a alteração tenha efeito."
            )
