# Em... src/assets/styles/filtroano.py

def get_filtro_container_style():
    """Retorna o CSS para o estado NORMAL do container do filtro."""
    return """
        QFrame {
            background-color: #F3F3F3;
            border: 1px solid #CCCCCC;
            border-radius: 5px;
        }
    """

def get_filtro_container_hover_style():
    """Retorna o CSS para o estado HOVER (mouse em cima) do container."""
    return """
        QFrame {
            background-color: #E0E0E0; /* Cor de fundo mais escura, igual ao hover dos botões */
            border: 1px solid #CCCCCC;
            border-radius: 5px;
        }
    """

def get_filtro_ano_combo_style():
    """Retorna o CSS para a QComboBox (sem borda e fundo transparente)."""
    return """
        QComboBox {
            border: none;
            background-color: transparent;
            /* Padding zerado para que o alinhamento programático funcione perfeitamente */
            padding: 0px; 
            color: #333333;
            font-size: 16px;
            font-weight: bold;
        }
        QComboBox::drop-down {
            border: none;
            padding-right: 5px;
        }
        QComboBox QAbstractItemView {
            border: 1px solid #CCCCCC;
            background-color: #F3F3F3;
            color: #333333;
            selection-background-color: #2C2F3F;
            selection-color: white;
            font-size: 14px;
        }
    """