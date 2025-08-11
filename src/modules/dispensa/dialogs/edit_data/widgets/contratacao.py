from PyQt6.QtWidgets import *

def number_to_text(number):
    numbers_in_words = ["um", "dois", "três", "quatro", "cinco", "seis", "sete", "oito", "nove", "dez", "onze", "doze"]
    return numbers_in_words[number - 1] 

def create_info_comprasnet(data):
    """Cria um box com informações de compras, com campos somente leitura."""
    comprasnet_group_box = QGroupBox("Informações Integradas ao ComprasNet")
    comprasnet_group_box.setStyleSheet("""
        QGroupBox {
            border: 1px solid #3C3C5A;
            border-radius: 10px;
            font-size: 16px;
            font-weight: bold;
            color: white;
            margin-top: 13px;
        }
        QGroupBox:title {
            subcontrol-origin: margin;
            padding: 0 3px;
        }
    """)
    
    comprasnet_layout = QVBoxLayout()

    # Função auxiliar para criar um layout de linha com label e campo de texto não editável
    def create_info_row(label_text, value):
        row_layout = QHBoxLayout()
        label = QLabel(label_text)
        edit = QLineEdit(value)
        edit.setReadOnly(True)
        row_layout.addWidget(label)
        row_layout.addWidget(edit)
        return row_layout

    # Adiciona as informações no layout do grupo
    comprasnet_layout.addLayout(create_info_row("Valor Homologado:", data.get("valor_homologado", "")))
    comprasnet_layout.addLayout(create_info_row("Última Atualização:", data.get("ultima_atualizacao", "")))
    comprasnet_layout.addLayout(create_info_row("Quantidade de Itens Homologados:", data.get("qtd_itens_homologados", "")))
    comprasnet_layout.addLayout(create_info_row("Itens Fracassados/Desertos:", data.get("itens_fracassados_desertos", "")))
    comprasnet_layout.addLayout(create_info_row("Itens Não Definidos:", data.get("itens_nao_definidos", "")))

    # Define o layout do QGroupBox
    comprasnet_group_box.setLayout(comprasnet_layout)

    return comprasnet_group_box
