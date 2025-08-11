from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import pandas as pd

def create_GrupoSIGDEM(data, icons):
    """Função principal que cria o QGroupBox para o SIGDEM com assunto e sinopse configurados."""
    grupoSIGDEM = QGroupBox("SIGDEM")
    layout = QVBoxLayout(grupoSIGDEM)
    grupoSIGDEM.setStyleSheet("""
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
    # Ícones para botões
    icon_copy = QIcon(icons["copy_1"])
    # Campo "Assunto"
    layout.addWidget(create_label("No campo “Assunto”:", font_size="12pt"))
    textEditAssunto = create_text_edit(f"{data.get('id_processo')} - Abertura de Processo [{data.get('objeto')}]", max_height=60)
    btnCopyAssunto = create_copy_button(icon_copy, lambda: copy_to_clipboard(textEditAssunto.toPlainText()))
    layoutHAssunto = create_horizontal_layout([textEditAssunto, btnCopyAssunto])
    layout.addLayout(layoutHAssunto)

    # Campo "Sinopse"
    layout.addWidget(create_label("No campo “Sinopse”:", font_size="12pt"))
    sinopse_text = f"Termo de Abertura referente à {data.get('tipo')} nº {data.get('numero')}/{data.get('ano')}, para {get_descricao_servico(data)} {data.get('objeto')}\n" \
                   f"Processo Administrativo NUP: {data.get('nup')}\n" \
                   f"Setor Demandante: {data.get('setor_responsavel')}"
    textEditSinopse = create_text_edit(sinopse_text, max_height=140)
    btnCopySinopse = create_copy_button(icon_copy, lambda: copy_to_clipboard(textEditSinopse.toPlainText()))
    layoutHSinopse = create_horizontal_layout([textEditSinopse, btnCopySinopse])
    layout.addLayout(layoutHSinopse)

    grupoSIGDEM.setLayout(layout)
    return grupoSIGDEM

# Funções auxiliares para criação de componentes
def create_label(text, font_size="10pt"):
    label = QLabel(text)
    label.setStyleSheet(f"font-size: {font_size};")
    return label

def create_text_edit(initial_text, max_height):
    text_edit = QTextEdit(initial_text)
    text_edit.setStyleSheet("font-size: 12pt;")
    text_edit.setMaximumHeight(max_height)
    return text_edit

def create_copy_button(icon, callback):
    button = QPushButton()
    button.setIcon(icon)
    button.setToolTip("Copiar texto para a área de transferência")
    button.setFixedSize(QSize(40, 40))
    button.setIconSize(QSize(25, 25))
    button.clicked.connect(callback)
    return button

def create_horizontal_layout(widgets):
    layout = QHBoxLayout()
    for widget in widgets:
        layout.addWidget(widget)
    return layout

def copy_to_clipboard(text):
    clipboard = QApplication.clipboard()
    clipboard.setText(text)
    QToolTip.showText(QCursor.pos(), "Texto copiado para a área de transferência.", msecShowTime=1500)

def get_descricao_servico(data):
    return "aquisição de" if data.get("material_servico") == "Material" else "contratação de empresa especializada em"

def create_utilidades_group(pasta_base, nome_pasta, icons, criar_e_abrir_pasta, alterar_diretorio_base, editar_modelo):
    """Função principal que cria o layout de utilidades com os botões configurados."""
    utilidades_layout = QHBoxLayout()
    utilidades_layout.setSpacing(0)
    utilidades_layout.setContentsMargins(0, 0, 0, 0)

    icon_pdf = QIcon(icons["pdf"])

    # Criação dos botões e adição ao layout
    criar_pasta_button = create_utilidade_button(
        text="Criar e Abrir Pasta",
        icon_path=icon_pdf,
        callback=criar_e_abrir_pasta,
        tooltip_text="Clique para criar a estrutura de pastas e abrir"
    )
    utilidades_layout.addWidget(criar_pasta_button, alignment=Qt.AlignmentFlag.AlignCenter)

    editar_registro_button = create_utilidade_button(
        text="Local de Salvamento",
        icon_path=icon_pdf,
        callback=alterar_diretorio_base,
        tooltip_text="Clique para alterar o local de salvamento dos arquivos"
    )
    utilidades_layout.addWidget(editar_registro_button, alignment=Qt.AlignmentFlag.AlignCenter)

    visualizar_pdf_button = create_utilidade_button(
        text="Editar Modelos",
        icon_path=icon_pdf,
        callback=editar_modelo,
        tooltip_text="Clique para editar os modelos dos documentos"
    )
    utilidades_layout.addWidget(visualizar_pdf_button, alignment=Qt.AlignmentFlag.AlignCenter)

    return utilidades_layout

# Funções auxiliares para criar componentes específicos

def create_utilidade_button(text, icon_path, callback, tooltip_text):
    """Cria um botão com ícone e callback, configurado para o layout de utilidades."""
    icon = QIcon(str(icon_path))
    button = QPushButton(text)
    button.setIcon(icon)
    button.setToolTip(tooltip_text)
    button.setFixedSize(QSize(210, 40))
    button.setIconSize(QSize(40, 40))
    button.clicked.connect(callback)
    return button