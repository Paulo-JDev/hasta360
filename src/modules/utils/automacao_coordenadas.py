# src/modules/utils/automacao_coordenadas.py

import pyautogui
import pyperclip
import time
from PyQt6.QtWidgets import QMessageBox
from modules.utils.coordinate_manager import CoordinateManager

from modules.utils.cc_manager import CCManager

def executar_automacao_email_coords(destinatario, ccs, assunto, corpo_mensagem):
    """
    Executa a automação de e-mail seguindo a sequência:
    Novo -> Para -> (Exibir CC) -> CC -> Assunto -> Corpo -> (Anexar) -> Enviar
    """
    manager = CoordinateManager()
    cc_manager = CCManager()
    
    print("\n--- INICIANDO AUTOMAÇÃO (PyAutoGUI) ---")

    # --- FUNÇÕES AUXILIARES ---
    def click_at(key, descricao, obrigatorio=True):
        coords = manager.get_coord(key)
        if not coords:
            if obrigatorio:
                QMessageBox.warning(None, "Configuração Faltando", 
                                    f"A posição do '{descricao}' não foi configurada.\n"
                                    "Vá em Configurações (Engrenagem) e capture a posição.")
            else:
                print(f"Pulo opcional: '{descricao}' não configurado.")
            return False
        
        print(f"Clicando em {descricao} ({coords})...")
        pyautogui.click(coords[0], coords[1])
        time.sleep(1.5) # Pausa padrão para o site carregar/reagir
        return True

    def paste_text(text):
        if not text: return
        pyperclip.copy(text)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)

    # --- INÍCIO DO FLUXO ---

    # 0. Aviso Inicial (Dá tempo do usuário soltar o mouse)
    print("Aguardando 3 segundos antes de começar...")
    time.sleep(3)

    # 1. Clicar em 'Novo Email'
    if not click_at("btn_novo_email", "Botão Novo Email"): return

    # 2. Campo 'Para'
    if not click_at("campo_para", "Campo Para"): return
    paste_text(destinatario)

    # 3. Campo 'CC'
    texto_ccs = cc_manager.get_formatted_string()
    
    if texto_ccs: # Só executa se tiver emails salvos no JSON
        if manager.get_coord("btn_exibir_cc"):
            click_at("btn_exibir_cc", "Botão Exibir CC", obrigatorio=False)
        
        if click_at("campo_cc", "Campo CC"):
            paste_text(texto_ccs) # Cola a lista que veio do JSON

    # 4. Campo 'Assunto'
    if not click_at("campo_assunto", "Campo Assunto"): return
    paste_text(assunto)

    # 5. Corpo do Email
    if not click_at("campo_corpo", "Corpo do Email"): return
    paste_text(corpo_mensagem)

    # 6. Botão 'Anexar' (Ainda não implementamos a seleção de arquivo, apenas o clique)
    # Deixei como opcional (obrigatorio=False) para não travar se você não configurar
    click_at("btn_anexar", "Botão Anexar", obrigatorio=False)

    # 7. Botão 'Enviar'
    # Comente a linha abaixo se quiser revisar antes de enviar automaticamente
    # click_at("btn_enviar", "Botão Enviar", obrigatorio=False)

    print("--- FIM DA AUTOMAÇÃO ---")
    QMessageBox.information(None, "Concluído", 
                            "Preenchimento finalizado!\n"
                            "Verifique os dados e anexe os arquivos manualmente se necessário.")
