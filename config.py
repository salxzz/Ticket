import json
import os

def load_config(file_path):
    if not os.path.exists(file_path):
        print(f"Erro: O arquivo '{file_path}' não foi encontrado.")
        return None

    try:
        with open(file_path, 'r') as f:
            config = json.load(f)
        return config
    except json.JSONDecodeError:
        print(f"Erro: O arquivo '{file_path}' está corrompido ou vazio.")
        return None

config_path = 'config.json'
config = load_config(config_path)

if config:
    category_open = config['category_open']
    category_closed = config['category_closed']
    cargo_perm = config['cargo_perm']
    logs = config['logs']
    entregas = config['entregas']
    cliente = config['cliente']
else:
    print("Falha ao carregar as configurações. Verifique o arquivo config.json.")
