import json
from pathlib import Path

# Define o caminho para salvar o JSON de coordenadas
# Salva em src/database/json/coordenadas.json
JSON_PATH = Path(__file__).resolve().parent.parent.parent / "database" / "json" / "coordenadas.json"

class CoordinateManager:
    def __init__(self):
        self.coords = self.load_coords()

    def load_coords(self):
        if not JSON_PATH.exists():
            return {}
        try:
            with open(JSON_PATH, 'r') as f:
                return json.load(f)
        except:
            return {}

    def save_coord(self, key, x, y):
        self.coords[key] = {"x": x, "y": y}
        # Garante que o diretório existe
        JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(JSON_PATH, 'w') as f:
            json.dump(self.coords, f, indent=4)

    def get_coord(self, key):
        """Retorna uma tupla (x, y) ou None se não existir."""
        data = self.coords.get(key)
        if data:
            return data["x"], data["y"]
        return None
