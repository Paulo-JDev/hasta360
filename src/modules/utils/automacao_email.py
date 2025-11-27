import pyautogui
import pyperclip
import time
from PyQt6.QtWidgets import QMessageBox
from modules.utils.coordinate_manager import CoordinateManager

def executar_automacao_email(destinatario, ccs, assunto, corpo_mensagem):
    """
    Executa a automação de e-mail usando coordenadas salvas.
    
    :param destinatario: E-mail do destinatário principal
    :param ccs: Lista de e-mails em cópia (ex: ['email1@teste.com', 'email2@teste.com'])
    :param assunto: Assunto do e-mail
    :param corpo_mensagem: Corpo do e-mail
    """
    manager = CoordinateManager()
    
    print("\n--- INICIANDO AUTOMAÇÃO DE E-MAIL (COORDENADAS) ---")

    # Função auxiliar para clicar em uma coordenada salva
    def click_at(key, descricao):
        coords = manager.get_coord(key)
        if not coords:
            QMessageBox.warning(None, "Configuração Necessária", 
                                f"A posição do '{descricao}' não foi configurada.\n"
                                "Vá em Configurações (Engrenagem) > Automação e configure.")
            return False
        
        print(f"Clicando em {descricao} na posição {coords}...")
        pyautogui.click(coords[0], coords[1])
        time.sleep(1.0) # Pausa para a interface reagir
        return True

    # Função auxiliar para colar texto
    def paste_text(text):
        pyperclip.copy(text)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)

    # --- PASSO 1: Clicar em 'Novo Email' ---
    if not click_at("btn_novo_email", "Botão Novo Email"): return

    # --- PASSO 2: Clicar e Preencher 'Para' ---
    if not click_at("campo_para", "Campo Para"): return
    paste_text(destinatario)

    # --- PASSO 3: Clicar e Preencher 'CC' (Cópia) ---
    # Só executa se houver CCs para adicionar
    if ccs and len(ccs) > 0:
        # Clica no botão que abre o campo CC (se necessário no seu webmail)
        if not click_at("btn_exibir_cc", "Botão Exibir CC"): return
        
        # Clica no campo CC
        if not click_at("campo_cc", "Campo CC"): return
        
        # Junta os e-mails com ponto e vírgula (padrão de e-mail)
        texto_cc = "; ".join(ccs)
        paste_text(texto_cc)

    # --- PASSO 4: Clicar e Preencher 'Assunto' ---
    if not click_at("campo_assunto", "Campo Assunto"): return
    paste_text(assunto)

    # --- PASSO 5: Clicar e Preencher 'Corpo' ---
    if not click_at("campo_corpo", "Corpo do Email"): return
    paste_text(corpo_mensagem)

    # --- PASSO 6 (Opcional): Anexar Arquivos ---
    # (Podemos adicionar depois se precisar)

    print("--- AUTOMAÇÃO CONCLUÍDA ---")
    QMessageBox.information(None, "Sucesso", "O e-mail foi preenchido com sucesso!\nVerifique e clique em enviar.")
