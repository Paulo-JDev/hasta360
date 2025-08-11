# paths/__init__.py

# Importando diretamente os objetos ou funções de cada módulo interno
from .base_path import *
from .config_path import *
from .atas import *
from .dispensa import *
from .contratos import *
from .planejamento  import *

# Definindo __all__ para controle explícito do que será exportado
__all__ = [
    # base_path
    "BASE_DIR", "CONFIG_FILE", "DATABASE_DIR", "MODULES_DIR", "JSON_DIR", "SQL_DIR", 
    "ASSETS_DIR", "TEMPLATE_DIR", "STYLE_PATH", "ICONS_DIR", "CONTROLE_DADOS",
    
    # dispensa_path
    "DATA_DISPENSA_ELETRONICA_PATH", "TEMPLATE_DISPENSA_DIR",

    # contratos
    "DATA_CONTRATOS_PATH", "TEMPLATE_CONTRATOS_DIR",

    # planejamento
    "DATA_PLANEJAMENTO_PATH", "TEMPLATE_PLANEJAMENTO_DIR",

    # atas_path
    "TEMPLATE_PATH", "DATA_ATAS_PATH",
    "CONFIG_API_FILE", "DATA_ATAS_API_PATH",
    
    # config_path
    "PRE_DEFINICOES_JSON", "ORGANIZACOES_FILE", "AGENTES_RESPONSAVEIS_FILE", "PDF_DIR",
    ]
