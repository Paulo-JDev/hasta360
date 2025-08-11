import locale
from PyQt6.QtWidgets import QLineEdit

# Define o locale para BRL
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def formatar_para_brl(valor):
    """Converte o valor para o formato BRL."""
    try:
        # Trata diferentes formatos de entrada
        if valor is None or valor == "":
            return "R$ 0,00"
        if isinstance(valor, str):
            valor = float(valor.replace('R$', '').replace('.', '').replace(',', '.').strip())
        return locale.currency(valor, grouping=True, symbol=True)
    except ValueError:
        return "R$ 0,00"

class CustomQLineEdit(QLineEdit):
    def __init__(self, valor_inicial, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.valor_inicial = valor_inicial  # Armazena o valor inicial como número
        self.setText(formatar_para_brl(valor_inicial))  # Exibe o valor inicial formatado
        self.textChanged.connect(self.validar_valor)  # Valida quando o texto é alterado

    def validar_valor(self):
        """Valida o valor digitado e converte para float."""
        texto_atual = self.text().replace('R$', '').replace('.', '').replace(',', '.').strip()
        try:
            float(texto_atual)  # Apenas valida se é um número
        except ValueError:
            self.setStyleSheet("border: 1px solid red;")  # Indica erro visualmente
        else:
            self.setStyleSheet("")  # Remove o erro visual

    def focusOutEvent(self, event):
        """Override do evento focusOut para aplicar formatação BRL apenas se o valor for válido."""
        texto_atual = self.text().replace('R$', '').replace('.', '').replace(',', '.').strip()
        try:
            # Atualiza apenas se o valor for válido
            valor_numerico = float(texto_atual)
            self.setText(formatar_para_brl(valor_numerico))
        except ValueError:
            self.setText(formatar_para_brl(self.valor_inicial))  # Retorna ao valor inicial
        super().focusOutEvent(event)