import json
from pathlib import Path

# Define o caminho para salvar o JSON de e-mails CC
# Salva em src/database/json/cc_emails.json
JSON_PATH = Path(__file__).resolve().parent.parent.parent / "database" / "json" / "cc_emails.json"

class CCManager:
    def load_emails(self):
        """Retorna uma lista de strings (e-mails)."""
        if not JSON_PATH.exists():
            return []
        try:
            with open(JSON_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("emails", [])
        except:
            return []

    def save_emails(self, email_list):
        """Recebe uma lista de e-mails e salva no JSON."""
        # Garante que o diretório existe
        JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        # Limpa espaços e remove vazios
        clean_list = [e.strip() for e in email_list if e and str(e).strip()]
        
        data = {"emails": clean_list}
        
        with open(JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            
    def get_formatted_string(self):
        """Retorna os e-mails prontos para colar (separados por ponto e vírgula)."""
        emails = self.load_emails()
        return "; ".join(emails)