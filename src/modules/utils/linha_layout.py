from PyQt6.QtWidgets import QFrame, QSpacerItem, QSizePolicy, QVBoxLayout

def linha_divisoria_layout(color="#3C3C5A", height=1, spacing=10):
    """
    Cria uma linha divisória horizontal com espaçamento abaixo dela.

    Args:
        color (str): Cor de fundo da linha divisória.
        height (int): Altura da linha divisória.
        spacing (int): Altura do espaçamento abaixo da linha.

    Returns:
        tuple: Contendo o QFrame da linha divisória e o QSpacerItem de espaçamento.
    """
    # Linha divisória
    linha_divisoria = QFrame()
    linha_divisoria.setFrameShape(QFrame.Shape.HLine)
    linha_divisoria.setFrameShadow(QFrame.Shadow.Sunken)
    linha_divisoria.setFixedHeight(height)
    linha_divisoria.setStyleSheet(f"background-color: {color};")

    # Espaçador abaixo da linha divisória
    spacer_baixo_linha = QSpacerItem(20, spacing, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

    return linha_divisoria, spacer_baixo_linha

def linha_divisoria_sem_spacer_layout(color="#3C3C5A", height=1, spacing=10):
    """
    Cria uma linha divisória horizontal com espaçamento abaixo dela.

    Args:
        color (str): Cor de fundo da linha divisória.
        height (int): Altura da linha divisória.
        spacing (int): Altura do espaçamento abaixo da linha.

    Returns:
        tuple: Contendo o QFrame da linha divisória e o QSpacerItem de espaçamento.
    """
    # Linha divisória
    linha_divisoria = QFrame()
    linha_divisoria.setFrameShape(QFrame.Shape.HLine)
    linha_divisoria.setFrameShadow(QFrame.Shadow.Sunken)
    linha_divisoria.setFixedHeight(height)
    linha_divisoria.setStyleSheet(f"background-color: {color};")

    return linha_divisoria