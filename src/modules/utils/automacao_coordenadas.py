import pyautogui
import pyperclip
import time
from PyQt6.QtWidgets import QMessageBox

def executar_automacao_email_coords(destinatario, assunto, corpo_mensagem):
    """
    Executa uma sequência de automação baseada em coordenadas fixas para enviar um e-mail.
    """
    try:
        print("\n--- INICIANDO AUTOMAÇÃO DE E-MAIL POR COORDENADAS ---")

        # 1. Pausa inicial para o navegador abrir a aba
        print("Aguardando o navegador carregar (2 segundos)...")
        time.sleep(2)

        # 2. Clicar para abrir a tela de "Escrever E-mail"
        print("Clicando para compor o novo e-mail...")
        pyautogui.click(x=-1857, y=226)
        time.sleep(2)  # Pausa para a tela de composição de e-mail abrir

        # 3. Colar o destinatário
        # O cursor já deve estar no campo "Para:", então colamos diretamente.
        print(f"Colando destinatário: {destinatario}")
        pyperclip.copy(destinatario)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)

        # 4. Clicar no campo do corpo do e-mail
        # (A sua lógica de clicar no campo "Para:" como fallback é boa, mas
        # pular com 'tab' é mais confiável se os campos mudarem de lugar)
        print("Pulando para o campo do assunto...")
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab') # Geralmente pula do "Para" para o "Assunto"
        time.sleep(0.5)
        
        print(f"Colando assunto...")
        pyperclip.copy(assunto)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        
        print("Pulando para o corpo do e-mail...")
        pyautogui.click(x=-1745, y=437) # Geralmente pula do "Assunto" para o "Corpo"
        time.sleep(0.5)

        # 5. Colar a mensagem no corpo do e-mail
        print("Colando corpo da mensagem...")
        pyperclip.copy(corpo_mensagem)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)

        # 6. Clicar em Enviar
        print("Clicando no botão Enviar...")
        pyautogui.click(x=-1889, y=231)

        print("--- AUTOMAÇÃO FINALIZADA ---")
        QMessageBox.information(None, "Automação Concluída", "O e-mail foi preenchido e enviado.")

    except Exception as e:
        print(f"ERRO durante a automação com PyAutoGUI: {e}")
        QMessageBox.critical(None, "Erro na Automação", f"Ocorreu um erro durante a automação do mouse e teclado: {e}")