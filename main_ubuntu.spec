# main_ubuntu.spec
# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path
from PyInstaller.utils.hooks import collect_all

# Defina o caminho do diretório base diretamente
BASE_DIR = Path("C:/Users/gabri/OneDrive/Área de Trabalho/prog-estagio/git-comandante/360_homolog/src")
DATABASE_DIR = BASE_DIR / "database"
ASSETS_DIR = BASE_DIR / "assets"
ICON_PATH = ASSETS_DIR / "brasil.png"

# Adicione o caminho do diretório base ao sys.path
sys.path.insert(0, str(BASE_DIR))

block_cipher = None

a = Analysis(
    ['src/main.py'],  # Corrigido para o caminho correto
    pathex=[str(BASE_DIR)],
    binaries=[],
    datas=[(str(ICON_PATH), 'src/assets/')],  # Adiciona o ícone ao executável
    hiddenimports=['psutil'],
    hookspath=['.'], 
    runtime_hooks=[],
    excludes=['PyQt5'],
    cipher=block_cipher,
)

# Inclua os diretórios database e resources inteiros
a.datas += Tree(str(DATABASE_DIR), prefix='src/database/')
a.datas += Tree(str(ASSETS_DIR), prefix='src/assets/')

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='licitacao360',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir="assets",
    console=True,
    icon=str(ICON_PATH)  # Adiciona o ícone PNG
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='licitacao360',
)
