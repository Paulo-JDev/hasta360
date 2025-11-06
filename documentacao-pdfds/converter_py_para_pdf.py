import os
import sys
import tkinter as tk
from tkinter import filedialog
from fpdf import FPDF
import chardet  # <--- MUDANÇA AQUI (era 'import cchardet as chardet')

# --- Configuração ---
# Nome da pasta onde os PDFs serão salvos
PASTA_RAIZ_PDF = "PDF-documentos"
# --------------------

def detectar_codificacao(caminho_arquivo):
    """
    Detecta a codificação de um arquivo para evitar erros de leitura.
    Usa a biblioteca 'chardet' (versão pura Python).
    """
    try:
        with open(caminho_arquivo, 'rb') as f:
            raw_data = f.read()
            resultado = chardet.detect(raw_data) # <--- ESSA LINHA FUNCIONA IGUAL
            codificacao = resultado['encoding']
            
            # Se a detecção falhar, usar UTF-8 como padrão seguro
            return codificacao if codificacao else 'utf-8'
    except Exception:
        return 'utf-8' # Padrão em caso de erro

def criar_pdf_do_codigo(caminho_py, caminho_pdf):
    """
    Lê um arquivo .py e salva seu conteúdo em um PDF, usando fonte monoespaçada.
    """
    try:
        # Detecta a codificação e lê o arquivo
        codificacao = detectar_codificacao(caminho_py)
        with open(caminho_py, 'r', encoding=codificacao, errors='replace') as f:
            conteudo_codigo = f.read()

        # Configura o PDF
        pdf = FPDF()
        pdf.add_page()
        
        # Define uma fonte monoespaçada (boa para código)
        try:
            pdf.set_font("Courier", size=9)
        except RuntimeError:
            print("  Aviso: Fonte 'Courier' não encontrada, usando 'Arial'. A formatação do código pode não ser ideal.")
            pdf.set_font("Arial", size=9)

        # Adiciona o nome do arquivo como um título no PDF
        nome_arquivo = os.path.basename(caminho_py)
        pdf.set_font(style='B', size=12) # Negrito
        pdf.cell(0, 10, f"Arquivo: {nome_arquivo}", 0, 1, 'L')
        pdf.ln(5) # Pula uma linha
        
        # Adiciona o conteúdo do código
        pdf.set_font(style='', size=9) # Volta ao normal
        pdf.multi_cell(0, 5, conteudo_codigo)
        
        # Salva o PDF
        pdf.output(caminho_pdf)
        return True
        
    except Exception as e:
        print(f"  [ERRO] Falha ao converter {caminho_py}: {e}")
        return False

def selecionar_pasta_e_converter():
    """
    Função principal: Pede ao usuário para escolher uma pasta
    e inicia o processo de conversão.
    """
    # 1. Configura e oculta a janela principal do Tkinter
    root = tk.Tk()
    root.withdraw()

    # 2. Pede ao usuário para selecionar a pasta de origem
    print("Por favor, selecione a pasta que contém seus arquivos .py...")
    pasta_origem = filedialog.askdirectory(title="Selecione a pasta raiz dos seus projetos Python")

    if not pasta_origem:
        print("Nenhuma pasta selecionada. O programa será encerrado.")
        sys.exit()

    print(f"Pasta de origem selecionada: {pasta_origem}")
    
    # 3. Define o caminho absoluto da pasta de destino dos PDFs
    pasta_destino_abs = os.path.abspath(PASTA_RAIZ_PDF)
    os.makedirs(pasta_destino_abs, exist_ok=True)
    print(f"Os PDFs serão salvos em: {pasta_destino_abs}\n")
    print("Iniciando a conversão...")

    # 4. Percorre a árvore de diretórios da pasta de origem
    total_convertido = 0
    total_falha = 0
    
    for dirpath, dirnames, filenames in os.walk(pasta_origem):
        
        # 5. Filtra apenas arquivos .py
        arquivos_py = [f for f in filenames if f.endswith('.py')]
        
        if not arquivos_py:
            continue
            
        # 6. Calcula o caminho relativo (para espelhar a estrutura)
        caminho_relativo = os.path.relpath(dirpath, pasta_origem)
        
        # 7. Cria a pasta de destino espelhada
        if caminho_relativo == ".":
            pasta_destino_espelhada = pasta_destino_abs
        else:
            pasta_destino_espelhada = os.path.join(pasta_destino_abs, caminho_relativo)
            
        os.makedirs(pasta_destino_espelhada, exist_ok=True)
        
        # 8. Converte cada arquivo .py encontrado
        for nome_py in arquivos_py:
            caminho_py_completo = os.path.join(dirpath, nome_py)
            
            nome_pdf = os.path.splitext(nome_py)[0] + ".pdf"
            caminho_pdf_completo = os.path.join(pasta_destino_espelhada, nome_pdf)

            print(f"Convertendo: {os.path.relpath(caminho_py_completo, pasta_origem)}")
            
            if criar_pdf_do_codigo(caminho_py_completo, caminho_pdf_completo):
                total_convertido += 1
            else:
                total_falha += 1

    print("\n--- Processo Concluído ---")
    print(f"Arquivos convertidos com sucesso: {total_convertido}")
    print(f"Arquivos com falha: {total_falha}")
    print(f"Verifique a pasta '{pasta_destino_abs}'")

# --- Inicia o programa ---
if __name__ == "__main__":
    selecionar_pasta_e_converter()