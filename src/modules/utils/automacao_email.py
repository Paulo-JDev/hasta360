import pyautogui
import pyperclip
import time
from PyQt6.QtWidgets import QMessageBox
from modules.utils.coordinate_manager import CoordinateManager

def executar_automacao_email_coords(destinatario, ccs, assunto, corpo_mensagem):
    """
    Executa a automação seguindo a ordem:
    Novo Email -> Para -> (Exibir CC) -> CC -> Assunto -> Corpo -> (Anexar) -> Enviar
    """
    manager = CoordinateManager()
    
    print("\n--- INICIANDO AUTOMAÇÃO (COORDENADAS) ---")

    # --- FUNÇÕES AUXILIARES ---
    def click_at(key, descricao, obrigatorio=True):
        coords = manager.get_coord(key)
        # Se a coordenada for 0,0 ou inexistente, considera não configurada
        if not coords or (coords[0] == 0 and coords[1] == 0):
            if obrigatorio:
                QMessageBox.warning(None, "Configuração Faltando", 
                                    f"A posição do '{descricao}' ({key}) não foi configurada ou está zerada.\n"
                                    "Vá em Configurações (Engrenagem) e capture a posição.")
            return False
        
        print(f"(automação_email.py)Clicando em {descricao} na posição {coords}...")
        pyautogui.click(coords[0], coords[1])
        time.sleep(1.5) # Pausa para o site responder
        return True

    def paste_text(text):
        if not text: return
        pyperclip.copy(text)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)

    # 0. Aviso Inicial
    print("Aguardando o navegador (3s)...")
    time.sleep(3)

    # 1. Clicar em 'Novo Email'
    if not click_at("btn_novo_email", "Botão Novo Email"): return

    # 2. Campo 'Para'
    if not click_at("campo_para", "Campo Para"): return
    paste_text(destinatario)

    # 3. Campo 'CC' (Lógica Nova)
    # Só executa se houver CCs na lista passada
    if ccs and len(ccs) > 0:
        # Tenta clicar no botão de exibir CC (caso o webmail esconda o campo)
        # Se não tiver coordenada salva (0,0), ele apenas pula sem erro (obrigatorio=False)
        if manager.get_coord("btn_exibir_cc") != (0,0):
            click_at("btn_exibir_cc", "Botão Exibir CC", obrigatorio=False)
        
        # Clica no campo CC e cola
        if click_at("campo_cc", "Campo CC"):
            # Junta a lista de emails em uma única string separada por ponto e vírgula
            texto_cc = "; ".join(ccs) 
            paste_text(texto_cc)

    # 4. Campo 'Assunto'
    if not click_at("campo_assunto", "Campo Assunto"): return
    paste_text(assunto)

    # 5. Corpo do Email (Usa a chave correta 'campo_corpo')
    if not click_at("campo_corpo", "Corpo do Email"): return
    paste_text(corpo_mensagem)

    # 6. Botão 'Anexar' (Opcional por enquanto)
    # click_at("btn_anexar", "Botão Anexar", obrigatorio=False)

    # 7. Botão 'Enviar' (Opcional - Descomente para enviar automático)
    click_at("btn_enviar", "Botão Enviar", obrigatorio=False)

    print("--- FIM DA AUTOMAÇÃO ---")
    QMessageBox.information(None, "Concluído", "E-mail preenchido com sucesso!")
