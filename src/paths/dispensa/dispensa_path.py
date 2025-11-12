from ..base_path import *
from ..config_path import load_config  # Importa a função de carregar
from pathlib import Path

DISPENSA_DIR = MODULES_DIR / "dispensa"

# 1. Define o caminho padrão (caso o config.json não exista ou esteja vazio)
DEFAULT_DISPENSA_DB = SQL_DIR / "controle_contratacao_direta.db"

# 2. Carrega o caminho do config.json usando a chave "DISPENSA_DB_PATH"
#    Se a chave não for encontrada, usa o valor padrão.
DATA_DISPENSA_ELETRONICA_PATH = Path(load_config(
    "DISPENSA_DB_PATH", 
    str(DEFAULT_DISPENSA_DB)
))

TEMPLATE_DISPENSA_DIR = DISPENSA_DIR / "template"
