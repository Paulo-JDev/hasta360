import json
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QComboBox, QGroupBox
from PyQt6.QtCore import Qt
import pandas as pd

def create_combo_box(current_text, items, fixed_width, fixed_height):
    combo_box = QComboBox()
    combo_box.addItems(items)
    combo_box.setFixedWidth(fixed_width)
    combo_box.setFixedHeight(fixed_height)
    combo_box.setCurrentText(current_text)
    combo_box.setStyleSheet("""
        QComboBox {
            padding: 5px;
        }
    """)
    combo_box.setCursor(Qt.CursorShape.PointingHandCursor)
    combo_box.view().setCursor(Qt.CursorShape.PointingHandCursor)
    return combo_box

def carregar_agentes_responsaveis(json_file_path, combo_mapping):
    """Carrega os agentes responsáveis a partir do arquivo JSON."""
    try:
        with open(json_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for key, combo_widget in combo_mapping.items():
            if key == "NOT LIKE":
                json_key = "responsável_pela_demanda"
            elif "Ordenador de Despesa" in key:
                json_key = "ordenador_de_despesa"
            elif "Agente Fiscal" in key:
                json_key = "agente_fiscal"
            elif "Gerente de Crédito" in key:
                json_key = "gerente_de_crédito"
            elif "Operador" in key:
                json_key = "operador_da_contratação"
            else:
                continue

            combo_widget.clear()
            agentes = data.get(json_key, [])
            for agente in agentes:
                texto_display = f"{agente.get('Nome', '')}\n{agente.get('Posto', '')}\n{agente.get('Funcao', '')}"
                combo_widget.addItem(texto_display, userData=agente)
    except Exception as e:
        print(f"Erro ao carregar agentes responsáveis do arquivo JSON: {e}")
