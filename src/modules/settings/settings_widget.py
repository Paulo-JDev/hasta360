from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from pathlib import Path
# Importa a função para salvar a configuração
from paths.config_path import load_config, save_config
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

        self.email_group = QGroupBox("Configurações de E-mail (Gmail)")
        self.email_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        self.email_layout = QVBoxLayout()

        # Carrega os valores salvos ou usa os padrões que você forneceu
        current_email = load_config("GMAIL_USER", "ceimbratech@gmail.com")
        current_pass = load_config("GMAIL_APP_PASS", "") # A senha fica vazia por segurança
        current_cc1 = load_config("CC_EMAIL_1", "pedro.soares@marinha.mil.br")
        current_cc2 = load_config("CC_EMAIL_2", "teste.dasd@marinha.mil.br")

        # Campo E-mail do Remetente
        self.email_layout.addWidget(QLabel("E-mail do Remetente (Gmail):"))
        self.email_le = QLineEdit(current_email)
        self.email_le.setPlaceholderText("exemplo@gmail.com")
        self.email_layout.addWidget(self.email_le)

        # Campo Senha de App
        self.email_layout.addWidget(QLabel("Senha de App (16 dígitos):"))
        self.password_le = QLineEdit(current_pass)
        self.password_le.setEchoMode(QLineEdit.EchoMode.Password) # Esconde a senha
        self.password_le.setPlaceholderText("xxxx xxxx xxxx xxxx")
        self.email_layout.addWidget(self.password_le)

        # Campos de CC
        self.email_layout.addWidget(QLabel("E-mails em Cópia (CC) (Opcional):"))
        self.cc1_le = QLineEdit(current_cc1)
        self.cc1_le.setPlaceholderText("email_cc_1@dominio.com")
        self.email_layout.addWidget(self.cc1_le)
        
        self.cc2_le = QLineEdit(current_cc2)
        self.cc2_le.setPlaceholderText("email_cc_2@dominio.com")
        self.email_layout.addWidget(self.cc2_le)

        # Botão Salvar
        self.save_email_btn = QPushButton("Salvar Configurações de E-mail")
        self.save_email_btn.clicked.connect(self.save_email_config)
        self.email_layout.addWidget(self.save_email_btn)

        self.email_group.setLayout(self.email_layout)
        self.layout.addWidget(self.email_group)
        
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

    def save_email_config(self):
        """Salva as configurações de e-mail no config.json."""
        try:
            save_config("GMAIL_USER", self.email_le.text())
            save_config("GMAIL_APP_PASS", self.password_le.text())
            save_config("CC_EMAIL_1", self.cc1_le.text())
            save_config("CC_EMAIL_2", self.cc2_le.text())
            
            QMessageBox.information(
                self, 
                "Configuração Salva",
                "Configurações de e-mail salvas com sucesso!"
            )
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Erro ao Salvar",
                f"Não foi possível salvar as configurações:\n{e}"
            )
