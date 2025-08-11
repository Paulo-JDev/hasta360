from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import pandas as pd
from pathlib import Path
import fitz
import re
from num2words import num2words
import os
import sys
import subprocess
from datetime import datetime
from docxtpl import DocxTemplate
from PyPDF2 import PdfMerger
from paths import load_config_path_id, TEMPLATE_DISPENSA_DIR

class PDFAddDialog(QDialog):

    def __init__(self, dados, icons, pastas_necessarias, pasta_base, parent=None):
        super().__init__(parent)
        self.dados = dados  # Certifique-se de que 'dados' seja passado como parâmetro
        self.icons = icons
        self.pastas_necessarias = pastas_necessarias
        self.pasta_base = pasta_base

        # Configura ícones
        self.icon_existe = QIcon(self.icons["checked"])
        self.icon_nao_existe = QIcon(self.icons["cancel"])

        # Verifique se 'dados' é um DataFrame ou um dicionário e ajuste conforme necessário
        if isinstance(self.dados, pd.DataFrame):
            self.id_processo = self.dados['id_processo'].iloc[0]
            self.tipo = self.dados['tipo'].iloc[0]
            self.ano = self.dados['ano'].iloc[0]
            self.numero = self.dados['numero'].iloc[0]
            self.objeto = self.dados['objeto'].iloc[0]
        elif isinstance(self.dados, dict):
            self.id_processo = self.dados.get('id_processo')
            self.tipo = self.dados.get('tipo')
            self.ano = self.dados.get('ano')
            self.numero = self.dados.get('numero')
            self.objeto = self.dados.get('objeto')

        self.setWindowTitle('Adicionar PDF')
        self.setup_ui()

    def setup_ui(self):
        self.setFixedSize(1520, 780)  # Tamanho ajustado para acomodar todos os componentes

        # Layout principal vertical
        main_layout = QVBoxLayout(self)

        # Layout para a visualização, slider e QTreeWidget
        view_and_slider_and_tree_layout = QHBoxLayout()
        # Layout vertical para a visualização do PDF e botões de navegação
        pdf_view_layout = QVBoxLayout()

        # DraggableGraphicsView para visualizar o PDF
        self.pdf_view = DraggableGraphicsView()
        self.scene = QGraphicsScene()
        self.pdf_view.setScene(self.scene)
        self.pdf_view.setFixedSize(1000, 730)  # Tamanho da visualização do PDF
        pdf_view_layout.addWidget(self.pdf_view)

        # Botões de navegação de páginas abaixo da visualização do PDF
        navigation_widget = QWidget()
        nav_buttons_layout = QHBoxLayout(navigation_widget)
        
        self.prev_page_button = QPushButton("← Página Anterior")
        self.prev_page_button.clicked.connect(self.prev_page)

        # Inicializa o QLabel para o contador de páginas
        self.page_label = QLabel("1 de 1")
        self.page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.page_label.setStyleSheet("font-size: 14px; margin: 5px;")

        self.next_page_button = QPushButton("Próxima Página →")
        self.next_page_button.clicked.connect(self.next_page)

        # Adiciona os botões e o QLabel ao layout de navegação
        nav_buttons_layout.addWidget(self.prev_page_button)
        nav_buttons_layout.addWidget(self.page_label, 1)  # O argumento 1 faz com que o QLabel expanda para preencher o espaço
        nav_buttons_layout.addWidget(self.next_page_button)

        # Define o tamanho máximo para o widget de navegação
        navigation_widget.setMaximumWidth(980)

        # Adiciona o widget de navegação ao layout principal
        pdf_view_layout.addWidget(navigation_widget)

        # Adiciona o layout da visualização do PDF ao layout horizontal
        view_and_slider_and_tree_layout.addLayout(pdf_view_layout)
        
        # Slider de Zoom ao lado da visualização
        self.zoom_slider = QSlider(Qt.Orientation.Vertical)
        self.zoom_slider.setMinimum(50)  # 50% do zoom original
        self.zoom_slider.setMaximum(200)  # 200% do zoom original
        self.zoom_slider.setValue(50)  # Valor inicial do zoom (50%)
        self.zoom_slider.setTickPosition(QSlider.TickPosition.TicksRight)
        self.zoom_slider.setTickInterval(10)
        self.zoom_slider.valueChanged.connect(self.adjust_zoom)
        view_and_slider_and_tree_layout.addWidget(self.zoom_slider)

        # Layout vertical para o QTreeWidget e seus botões
        tree_layout = QVBoxLayout()

        # Cria e adiciona o cabeçalho acima do QTreeWidget
        header_widget = self.create_header()
        tree_layout.addWidget(header_widget)

        # QTreeWidget para exibir dados
        self.data_view = QTreeWidget()
        self.data_view.setHeaderHidden(True)
        self.data_view.setStyleSheet("""
            QTreeWidget::item { 
                height: 40px;
                font-size: 14px;
            }
        """)
        self.data_view.itemClicked.connect(self.display_pdf)
        tree_layout.addWidget(self.data_view)

        # Adiciona o layout do QTreeWidget ao layout horizontal principal
        view_and_slider_and_tree_layout.addLayout(tree_layout)

        # Adiciona o layout combinado ao layout principal
        main_layout.addLayout(view_and_slider_and_tree_layout)

        self.add_initial_items()

    def adjust_zoom(self, value):
        # Calcula o fator de escala baseado no valor do slider
        scale_factor = max(value / 100.0, 0.2)  # Garante que o fator de escala não seja menor que 0.5
        # Reseta a transformação atual e aplica o novo zoom
        self.pdf_view.resetTransform()
        self.pdf_view.scale(scale_factor, scale_factor)

    def verificar_arquivo_pdf(self, pasta):
        arquivos_pdf = []
        if not pasta.exists():
            print(f"Pasta não encontrada: {pasta}")
            return None
        for arquivo in pasta.iterdir():
            if arquivo.suffix.lower() == ".pdf":
                arquivos_pdf.append(arquivo)
                print(f"Arquivo PDF encontrado: {arquivo.name}")
        if arquivos_pdf:
            pdf_mais_recente = max(arquivos_pdf, key=lambda p: p.stat().st_mtime)
            print(f"PDF mais recente: {pdf_mais_recente}")
            return pdf_mais_recente
        return None
   
    def display_pdf(self, item, column):
        file_path = item.data(0, Qt.ItemDataRole.UserRole)
        if file_path:
            print(f"Tentando abrir o arquivo PDF: {file_path}")
            self.load_pdf(file_path)

    def load_pdf(self, file_path):
        try:
            self.document = fitz.open(file_path)  # Corrija o uso para fitz.open(file_path)
            self.current_page = 0  # Define a primeira página como a atual
            self.show_page(self.current_page)  # Mostra a primeira página
        except Exception as e:
            print(f"Erro ao abrir o arquivo PDF: {e}")

    def show_page(self, page_number):
        if self.document:
            page = self.document.load_page(page_number)
            mat = fitz.Matrix(5, 5)  # Ajuste para a escala desejada, mantém alta qualidade
            pix = page.get_pixmap(matrix=mat)
            img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(img)
            self.scene.clear()
            self.scene.addPixmap(pixmap)
            # Aplica o fator de escala inicial de 50%
            self.pdf_view.resetTransform()
            self.pdf_view.scale(0.5, 0.5)
            # Atualiza o contador de páginas
            self.page_label.setText(f"{page_number + 1} de {self.document.page_count}")

    def next_page(self):
        if self.document and self.current_page < self.document.page_count - 1:
            self.current_page += 1
            self.show_page(self.current_page)

    def prev_page(self):
        if self.document and self.current_page > 0:
            self.current_page -= 1
            self.show_page(self.current_page)

    def select_pdf_file(self):
        selected_item = self.data_view.currentItem()
        if selected_item:
            file_path, _ = QFileDialog.getOpenFileName(self, "Selecionar PDF", "", "PDF Files (*.pdf)")
            if file_path:
                selected_item.setText(0, selected_item.text(0))  # Atualiza o texto sem o caminho
                selected_item.setIcon(0, self.icon_existe)
                selected_item.setData(0, Qt.ItemDataRole.UserRole, file_path)  # Armazena o caminho do PDF
                self.save_file_paths()
            else:
                selected_item.setIcon(0, self.icon_nao_existe)

    def create_header(self):
        html_text = f"Anexos da {self.tipo} nº {self.numero}/{self.ano}<br>"
        
        self.titleLabel = QLabel()
        self.titleLabel.setTextFormat(Qt.TextFormat.RichText)
        self.titleLabel.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.titleLabel.setText(html_text)

        self.header_layout = QHBoxLayout()
        self.header_layout.addWidget(self.titleLabel)

        header_widget = QWidget()
        header_widget.setLayout(self.header_layout)

        return header_widget

    def add_initial_items(self):
        id_processo_modificado = self.id_processo.replace("/", "-")
        objeto_modificado = self.objeto.replace("/", "-")
        base_path = self.pasta_base / f'{id_processo_modificado} - {objeto_modificado}'

        initial_items = {
            "DFD": [
                ("Anexo A - Relatório Safin", base_path / '2. CP e anexos' / 'DFD' / 'Anexo A - Relatorio Safin'),
                ("Anexo B - Especificações e Quantidade", base_path / '2. CP e anexos' / 'DFD' / 'Anexo B - Especificações e Quantidade')
            ],
            "TR": [
                ("Pesquisa de Preços", base_path / '2. CP e anexos' / 'TR' / 'Pesquisa de Preços')
            ],
            "Declaração de Adequação Orçamentária": [
                ("Relatório do PDM-Catser", base_path / '2. CP e anexos' / 'Declaracao de Adequação Orçamentária' / 'Relatório do PDM-Catser')
            ]
        }

        for parent_text, children in initial_items.items():
            parent_item = QTreeWidgetItem(self.data_view, [parent_text])
            parent_item.setFont(0, QFont('SansSerif', 14))
            for child_text, pasta in children:
                child_item = QTreeWidgetItem(parent_item, [child_text])
                child_item.setForeground(0, QBrush(QColor(0, 0, 0)))
                child_item.setFont(0, QFont('SansSerif', 14))

                print(f"Verificando pasta: {pasta}")
                pdf_file = self.verificar_arquivo_pdf(pasta)
                if pdf_file:
                    print(f"PDF encontrado: {pdf_file}")
                    child_item.setIcon(0, self.icon_existe)
                    child_item.setData(0, Qt.ItemDataRole.UserRole, str(pdf_file))  # Armazena o caminho do PDF
                else:
                    print("Nenhum PDF encontrado")
                    child_item.setIcon(0, self.icon_nao_existe)

            parent_item.setExpanded(True)

class DraggableGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        self._panning = False
        self._last_mouse_position = QPoint()
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)  # Zoom focalizado no cursor do mouse

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._panning = True
            self._last_mouse_position = event.pos()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._panning:
            delta = event.pos() - self._last_mouse_position
            self._last_mouse_position = event.pos()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._panning = False
            self.setCursor(Qt.CursorShape.ArrowCursor)
        super().mouseReleaseEvent(event)

    def wheelEvent(self, event):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:  # Verifica se o Ctrl está pressionado
            factor = 1.15 if event.angleDelta().y() > 0 else 0.85  # Ajusta o fator de zoom baseado na direção do scroll
            scale = self.transform().m11() * factor
            if scale >= 0.1:  # Garante que o fator de escala não seja menor que 0.5
                self.scale(factor, factor)
        else:
            super().wheelEvent(event) 

class Worker(QThread):
    update_status = pyqtSignal(str, str, int) 
    task_complete = pyqtSignal()

    def __init__(self, documentos_encontrados, documentos, dados, icons, parent=None):
        super().__init__(parent)
        self.relacao_documentos_encontrados = documentos_encontrados  # Lista de documentos encontrados passada para o Worker
        self.documentos = documentos
        self.config = load_config_path_id()
        self.dados = dados
        self.pasta_base = Path(self.config.get('pasta_base', str(Path.home() / 'Desktop')))
        self.id_processo = self.dados.get('id_processo', '').replace('/', '-')
        self.objeto = self.dados.get('objeto', '').replace('/', '-')
        self.icons = icons
        self.pdf_paths = []

    def run(self):
        pdf_paths = []

        for doc in self.documentos:
            doc_desc = doc.get('desc', doc.get('subfolder', 'Documento desconhecido'))

            # Loop para atualizar os pontos dinamicamente
            for i in range(3):
                status = "sendo gerado" + "." * i
                self.update_status.emit(doc_desc, status, 50)

            if "template" in doc:
                docx_path = self.gerarDocumento(doc["template"], doc["subfolder"], doc["desc"])
                if docx_path:
                    pdf_path = self.salvarPDF(docx_path)
                    if pdf_path:
                        pdf_info = {"pdf_path": pdf_path}
                        if "cover" in doc:
                            pdf_info["cover_path"] = TEMPLATE_DISPENSA_DIR / doc["cover"]
                        pdf_paths.append(pdf_info)
            else:
                pdf_path = self.get_latest_pdf(self.pasta_base / self.nome_pasta / doc["subfolder"])
                if pdf_path:
                    pdf_paths.append({"pdf_path": pdf_path, "cover_path": TEMPLATE_DISPENSA_DIR / doc["cover"]})
                else:
                    error_msg = f"Arquivo PDF não encontrado: {doc['subfolder']}"
                    print(error_msg) 

            # Atualiza o status para "concluído" e emite o sinal para mudar o ícone
            self.update_status.emit(doc_desc, "concluído", 100)

        self.concatenar_e_abrir_pdfs(pdf_paths)
        self.task_complete.emit()

    def concatenar_e_abrir_pdfs(self, pdf_paths):
        if not pdf_paths:
            QMessageBox.warning(None, "Erro", "Nenhum PDF foi gerado para concatenar.")
            return

        output_pdf_path = self.pasta_base / self.nome_pasta / "2. CP e anexos" / "CP_e_anexos.pdf"
        merger = PdfMerger()

        try:
            for pdf in pdf_paths:
                if "cover_path" in pdf:
                    merger.append(str(pdf["cover_path"]))
                merger.append(str(pdf["pdf_path"]))

            merger.write(str(output_pdf_path))
            merger.close()

            # Abre o PDF utilizando QDesktopServices (multiplataforma)
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(output_pdf_path)))
            print(f"PDF concatenado salvo e aberto: {output_pdf_path}")
        except Exception as e:
            print(f"Erro ao concatenar os PDFs: {e}")
            QMessageBox.warning(None, "Erro", f"Erro ao concatenar os PDFs: {e}")

    def get_latest_pdf(self, directory):
        pdf_files = list(directory.glob("*.pdf"))
        if not pdf_files:
            return None
        latest_pdf = max(pdf_files, key=os.path.getmtime)
        return latest_pdf

    def alterar_posto(self, posto):
        # Define um dicionário de mapeamento de postos e suas respectivas abreviações
        mapeamento_postos = {
            r'Capitão[\s\-]de[\s\-]Corveta': 'CC',
            r'Capitão[\s\-]de[\s\-]Fragata': 'CF',
            r'Capitão[\s\-]de[\s\-]Mar[\s\-]e[\s\-]Guerra': 'CMG',
            r'Capitão[\s\-]Tenente': 'CT',
            r'Primeiro[\s\-]Tenente': '1ºTen',
            r'Segundo[\s\-]Tenente': '2ºTen',
            r'Primeiro[\s\-]Sargento': '1ºSG',
            r'Segundo[\s\-]Sargento': '2ºSG',
            r'Terceiro[\s\-]Sargento': '3ºSG',
            r'Cabo': 'CB',
            r'Sub[\s\-]oficial': 'SO',
        }

        # Itera sobre o dicionário de mapeamento e aplica a substituição
        for padrao, substituicao in mapeamento_postos.items():
            if re.search(padrao, posto, re.IGNORECASE):
                return re.sub(padrao, substituicao, posto, flags=re.IGNORECASE)

        # Retorna o posto original se nenhuma substituição for aplicada
        return posto

    def valor_por_extenso(self, valor):
        if not valor or valor.strip() == '':  # Verifica se o valor está vazio ou None
            return None  # Retorna None se o valor não for válido

        try:
            valor = valor.replace('R$', '').replace('.', '').replace(',', '.').strip()
            valor_float = float(valor)
            parte_inteira = int(valor_float)
            parte_decimal = int(round((valor_float - parte_inteira) * 100))

            if parte_decimal > 0:
                valor_extenso = f"{num2words(parte_inteira, lang='pt_BR')} reais e {num2words(parte_decimal, lang='pt_BR')} centavos"
            else:
                valor_extenso = f"{num2words(parte_inteira, lang='pt_BR')} reais"

            # Corrige "um reais" para "um real"
            valor_extenso = valor_extenso.replace("um reais", "um real")

            return valor_extenso

        except ValueError:
            return None

    def gerarDocumento(self, template, subfolder, desc):
        # Caminhos dos templates e do arquivo a ser salvo
        template_filename = f"template_{template}.docx"
        template_path, save_path = self.setup_document_paths(template_filename, subfolder, desc)

        # # Verificar e criar as pastas necessárias
        # self.verificar_e_criar_pastas(self.pasta_base / self.nome_pasta)

        # Verifica se o template existe
        if not template_path.exists():
            QMessageBox.warning(None, "Erro de Template", f"O arquivo de template não foi encontrado: {template_path}")
            return

        # Carregar e renderizar o template
        with open(str(template_path), 'rb') as template_file:
            doc = DocxTemplate(template_file)
            context = self.prepare_context(self.dados, self.relacao_documentos_encontrados)
            doc.render(context)
            doc.save(str(save_path))

        return save_path

    def prepare_context(self, data, documentos_encontrados):
        # Cria o contexto com os dados, convertendo valores None para 'Não especificado'
        context = {key: (str(value) if value is not None else 'Não especificado') for key, value in data.items()}
        
        # Descrição do serviço, dependendo do tipo de material
        descricao_servico = "aquisição de" if data['material_servico'] == "Material" else "contratação de empresa especializada em"
        descricao_servico_primeira_letra_maiuscula = descricao_servico[0].upper() + descricao_servico[1:]
        context.update({'descricao_servico': descricao_servico})
        context.update({'descricao_servico_primeira_letra_maiuscula': descricao_servico_primeira_letra_maiuscula})

        # Adiciona a lista de anexos ao contexto para ser usada no template
        # A lista de anexos é passada como uma string única com quebras de linha entre os itens
        context.update({'lista_anexos': "\n".join(documentos_encontrados)})

        # Processar responsável pela demanda e operador
        self.formatar_responsavel('responsavel_pela_demanda', data, context)
        self.formatar_responsavel('operador', data, context)

        # Processa o valor total e o converte para extenso
        valor_total = data.get('valor_total')
        if valor_total and isinstance(valor_total, str):
            valor_extenso = self.valor_por_extenso(valor_total)
            valor_total_e_extenso = f"{valor_total} ({valor_extenso})"
            context.update({'valor_total_e_extenso': valor_total_e_extenso})
        else:
            context.update({'valor_total_e_extenso': 'Não especificado'})

        # Lógica para atividade_custeio
        if data.get('atividade_custeio') == 'Sim':
            texto_custeio = (
                "A presente contratação por dispensa de licitação está enquadrada como atividade de custeio, "
                "conforme mencionado no artigo 2º da Portaria ME nº 7.828, de 30 de agosto de 2022. "
                "Conforme previsão do art. 3º do Decreto nº 10.193, de 27 de dezembro de 2019, e as normas "
                "infralegais de delegação de competência no âmbito da Marinha, que estabelecem limites e instâncias "
                "de governança, essa responsabilidade é delegada ao ordenador de despesas, respeitando os valores "
                "estipulados no decreto."
            )
        else:
            texto_custeio = (
                "A presente contratação por dispensa de licitação não se enquadra nas hipóteses de atividades de "
                "custeio previstas no Decreto nº 10.193, de 27 de dezembro de 2019, pois o objeto contratado não se "
                "relaciona diretamente às atividades comuns de suporte administrativo mencionadas no artigo 2º da "
                "Portaria ME nº 7.828, de 30 de agosto de 2022."
            )
        context.update({'texto_custeio': texto_custeio})

        # Alterar formato de data_sessao
        data_sessao = data.get('data_sessao')
        if data_sessao:
            try:
                data_obj = datetime.strptime(data_sessao, '%Y-%m-%d')
                dia_semana = data_obj.strftime('%A')
                data_formatada = data_obj.strftime('%d/%m/%Y') + f" ({dia_semana})"
                context.update({'data_sessao_formatada': data_formatada})
            except ValueError as e:
                context.update({'data_sessao_formatada': 'Data inválida'})
                print("Erro ao processar data da sessão:", e)
        else:
            context.update({'data_sessao_formatada': 'Não especificado'})
            print("Data da sessão não especificada")

        return context


    def setup_document_paths(self, template_filename, subfolder_name, file_description):
        """
        Configura os caminhos para os templates e os documentos gerados.
        """
        template_path = TEMPLATE_DISPENSA_DIR / template_filename
        self.nome_pasta = f"{self.id_processo} - {self.objeto}"

        # Verifica ou altera o diretório base
        if 'pasta_base' not in self.config:
            self.alterar_diretorio_base()

        # Define o caminho para salvar o arquivo gerado
        pasta_base = Path(self.config['pasta_base']) / self.nome_pasta / subfolder_name
        pasta_base.mkdir(parents=True, exist_ok=True)
        save_path = pasta_base / f"{self.id_processo} - {file_description}.docx"

        return template_path, save_path

    def verificar_e_criar_pastas(self, pasta_base):
        id_processo_modificado = self.id_processo.replace("/", "-")
        objeto_modificado = self.objeto.replace("/", "-")
        base_path = pasta_base / f'{id_processo_modificado} - {objeto_modificado}'

        pastas_necessarias = [
            pasta_base / '1. Autorizacao',
            pasta_base / '2. CP e anexos',
            pasta_base / '3. Aviso',
            pasta_base / '2. CP e anexos' / 'DFD',
            pasta_base / '2. CP e anexos' / 'DFD' / 'Anexo A - Relatorio Safin',
            pasta_base / '2. CP e anexos' / 'DFD' / 'Anexo B - Especificações e Quantidade',
            pasta_base / '2. CP e anexos' / 'TR',
            pasta_base / '2. CP e anexos' / 'TR' / 'Pesquisa de Preços',
            pasta_base / '2. CP e anexos' / 'Declaracao de Adequação Orçamentária',
            pasta_base / '2. CP e anexos' / 'Declaracao de Adequação Orçamentária' / 'Relatório do PDM-Catser',
            pasta_base / '2. CP e anexos' / 'ETP',
            pasta_base / '2. CP e anexos' / 'MR',
            pasta_base / '2. CP e anexos' / 'Justificativas Relevantes',
        ]
        for pasta in pastas_necessarias:
            if not pasta.exists():
                pasta.mkdir(parents=True)
        return pastas_necessarias

    def salvarPDF(self, docx_path):
        """
        Converte um arquivo .docx em PDF.
        """
        try:
            # Converte o caminho para Path, se necessário.
            docx_path = Path(docx_path) if not isinstance(docx_path, Path) else docx_path
            pdf_path = docx_path.with_suffix('.pdf')

            if sys.platform.startswith("win"):
                import win32com.client
                word = win32com.client.Dispatch("Word.Application")
                doc = None
                try:
                    doc = word.Documents.Open(str(docx_path))
                    doc.SaveAs(str(pdf_path), FileFormat=17)  # 17 é o código para PDF
                except Exception as e:
                    raise e
                finally:
                    if doc is not None:
                        doc.Close()
                    word.Quit()
            else:
                try:
                    comando = [
                        "libreoffice",
                        "--headless",
                        "--convert-to", "pdf",
                        "--outdir", str(docx_path.parent),
                        str(docx_path)
                    ]
                    subprocess.run(comando, check=True)
                except Exception as e:
                    raise e

            if not pdf_path.exists():
                raise FileNotFoundError(f"O arquivo PDF não foi criado: {pdf_path}")

            return pdf_path

        except Exception as e:
            print(f"Erro ao converter o documento: {e}")
            QMessageBox.warning(None, "Erro", f"Erro ao converter o documento: {e}")
            return None

    def formatar_responsavel(self, chave, data, context):
        responsavel = data.get(chave)
        if responsavel and isinstance(responsavel, str):
            try:
                nome, posto, funcao = responsavel.split('\n')
                posto_alterado = self.alterar_posto(posto)
                responsavel_dict = {
                    'nome': nome,
                    'posto': posto_alterado,
                }
                responsavel_extenso = f"{responsavel_dict.get('posto', '')} {responsavel_dict.get('nome', '')}"
                context.update({f'{chave}_formatado': responsavel_extenso})
            except ValueError:
                context.update({f'{chave}_formatado': 'Não especificado\nNão especificado'})
        else:
            context.update({f'{chave}_formatado': 'Não especificado\nNão especificado'})

class ProgressDialog(QDialog):
    def __init__(self, documentos_encontratos, documentos, icons, dados):
        super().__init__()
        self.setWindowTitle("Progresso")
        self.setFixedSize(500, 300)
        self.layout = QVBoxLayout(self)
        self.dados = dados

        # Inicializa os labels e ícones para cada documento
        self.labels = {}
        self.icons = icons

        self.icon_loading = QIcon(self.icons["loading_table"])  # Ícone para carregamento
        self.icon_done = QIcon(self.icons["aproved"])  # Ícone para conclusão

        # Adiciona os labels e ícones para cada documento com 'template'
        for doc in documentos:
            if "template" in doc:  # Somente para documentos que têm a chave 'template'
                doc_desc = doc.get('desc', doc.get('subfolder', 'Documento desconhecido'))

                layout_h = QHBoxLayout()

                # Cria o QLabel para o texto do documento e ajusta o estilo
                label = QLabel(f"{doc_desc}")
                label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)  # Alinha o texto verticalmente ao centro e à esquerda
                label.setStyleSheet("font-size: 14px;")  # Define o tamanho da fonte para 14px

                # Cria o QLabel para o ícone e alinha ao centro verticalmente
                icon_label = QLabel()
                icon_label.setPixmap(self.icon_loading.pixmap(24, 24))  # Tamanho do ícone: 24x24
                icon_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)  # Alinha o ícone verticalmente ao centro

                layout_h.addWidget(icon_label)
                layout_h.addWidget(label)
                layout_h.addStretch()  # Adiciona um espaçador para garantir que o texto e ícone fiquem à esquerda
                self.layout.addLayout(layout_h)

                # Armazena os labels e ícones para atualizá-los mais tarde
                self.labels[doc_desc] = label
                self.icons[doc_desc] = icon_label

        # Layout para "Consolidar Documentos PDFs"
        layout_h_consolidar = QHBoxLayout()

        # Cria o QLabel para o texto "Consolidar Documentos PDFs"
        self.label_consolidar = QLabel("Consolidação de Documentos.")
        self.label_consolidar.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.label_consolidar.setStyleSheet("font-size: 14px;")

        # Cria o QLabel para o ícone de carregamento
        self.icon_label_consolidar = QLabel()
        self.icon_label_consolidar.setPixmap(self.icon_loading.pixmap(24, 24))  # Exibe o ícone de carregamento inicialmente
        self.icon_label_consolidar.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        layout_h_consolidar.addWidget(self.icon_label_consolidar)
        layout_h_consolidar.addWidget(self.label_consolidar)
        layout_h_consolidar.addStretch()
        self.layout.addLayout(layout_h_consolidar)

        # Adiciona a barra de progresso indeterminada
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 0)  # Define a barra como indeterminada
        self.layout.addWidget(self.progress_bar)

        # Botão de fechar
        self.close_button = QPushButton("Fechar")
        self.close_button.setEnabled(False)
        self.close_button.clicked.connect(self.close)
        self.layout.addWidget(self.close_button)

        # Passe o df_registro_selecionado para o Worker
        self.worker = Worker(documentos_encontratos, documentos, self.dados, self.icons)
        self.worker.update_status.connect(self.update_label)
        self.worker.task_complete.connect(self.on_task_complete)  # Conectar ao novo método
        self.worker.task_complete.connect(self.enable_close_button)

        self.worker.start()

    @pyqtSlot(str, str, int)
    def update_label(self, doc_desc, status_text, progress):
        """
        Atualiza o texto do label e o ícone correspondente.
        """
        # Atualiza o label de progresso
        label = self.labels.get(doc_desc)
        if label:
            label.setText(f"{doc_desc} {status_text}")
        
        # Atualiza o ícone após a conclusão do documento
        if progress == 100:
            icon_label = self.icons.get(doc_desc)
            if icon_label:
                icon_label.setPixmap(self.icon_done.pixmap(24, 24))  # Altera para o ícone de 'concluído'

    @pyqtSlot()
    def enable_close_button(self):
        self.close_button.setEnabled(True)

    @pyqtSlot()
    def on_task_complete(self):
        """
        Atualiza o ícone de "Consolidar Documentos PDFs" quando o processo de consolidação for concluído.
        """
        self.label_consolidar.setText("Consolidação de Documentos (concluído)")
        self.icon_label_consolidar.setPixmap(self.icon_done.pixmap(24, 24))  # Altera para o ícone de 'concluído'

        # Oculta a barra de progresso quando o processo for concluído
        self.progress_bar.hide()


