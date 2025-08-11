from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from modules.utils.add_button import create_button
from modules.dispensa.dialogs.edit_data.apoio_data import STYLE_GROUP_BOX
from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton

def setup_consulta_api(parent, icons, data, max_width=300):
    """Configura o layout para consulta à API com campos de CNPJ e Sequencial PNCP."""
    group_box = QGroupBox("Consulta API", parent)
    group_box.setMaximumWidth(max_width)
    layout = QVBoxLayout(group_box)

    # Aplicando o estilo CSS específico ao GroupBox
    group_box.setStyleSheet(STYLE_GROUP_BOX)
    # Layout para CNPJ Matriz
    cnpj_layout = QHBoxLayout() 
    label_cnpj = QLabel("CNPJ Matriz:", parent)
    label_cnpj.setStyleSheet("color: #8AB4F7; font-size: 16px")
    cnpj_layout.addWidget(label_cnpj)

    cnpj_edit = QLineEdit(str(data.get('cnpj_matriz', '00394502000144')))
    cnpj_layout.addWidget(cnpj_edit)

    # Adiciona o layout do CNPJ ao layout principal
    layout.addLayout(cnpj_layout)

    # Layout para Sequencial PNCP
    sequencial_layout = QHBoxLayout()
    label_sequencial = QLabel("Sequencial PNCP:", parent)
    label_sequencial.setStyleSheet("color: #8AB4F7; font-size: 16px")
    sequencial_layout.addWidget(label_sequencial)

    sequencial_edit = QLineEdit(str(data.get('sequencial_pncp', '')))
    sequencial_edit.setPlaceholderText("Digite o Sequencial PNCP")
    sequencial_layout.addWidget(sequencial_edit)

    # Adiciona o layout do Sequencial ao layout principal
    layout.addLayout(sequencial_layout)

    # Botão de consulta usando a função create_button com ícone
    btn_consultar = create_button(
        text="Consultar",
        icon=icons.get("api", None),  # Ícone obtido diretamente
        callback=lambda: consultar_api(cnpj_edit),
        tooltip_text="Clique para consultar dados usando o CNPJ e Sequencial PNCP",
        parent=parent
    )
    layout.addWidget(btn_consultar)

    return group_box, cnpj_edit, sequencial_edit

def consultar_api(cnpj_edit):
    """Função de exemplo para consulta à API. Substitua pela lógica real."""
    cnpj = cnpj_edit.text()
    print(f"Consultando API com o CNPJ: {cnpj}")
    # Implementar a lógica de consulta à API aqui
    
def on_link_pncp_clicked(link_pncp, cnpj, ano):
    # Montando a URL
    url = f"https://pncp.gov.br/app/editais/{cnpj}/{ano}/{link_pncp}"

    # Abrindo o link no navegador padrão
    QDesktopServices.openUrl(QUrl(url))