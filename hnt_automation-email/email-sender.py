import json
import requests
import os
import time
import re
from tqdm import tqdm

def update_email_in_file(file_path, email):
    """Lê o arquivo linha por linha, atualiza o email e retorna a linha onde o email foi encontrado."""
    with open(file_path, 'r') as file:
        lines = file.readlines()

    email_line_numbers = []
    for idx, line in enumerate(lines):
        if re.search(r'"email"\s*:', line):
            # Atualizando o email sem usar look-behind
            lines[idx] = re.sub(r'("email"\s*:)\s*"[^"]*"', r'\1 "{}"'.format(email), line)
            email_line_numbers.append(idx + 1)  # Adicionando 1 porque a indexação começa em 0

    with open(file_path, 'w') as file:
        file.writelines(lines)

    return email_line_numbers

# 1. Ler o arquivo configs.json e extrair os valores.
with open("configs.json", "r") as file:
    config = json.load(file)

account = config["account"]
token = config["X-VTEX-API-AppToken"]
key = config["X-VTEX-API-AppKey"]
template_names = config["template-name"]

# 2. Perguntar o email de destino ao usuário.
email = input("Por favor, insira o email de destino: ")

headers = {
    "Content-Type": "application/json",
    "X-VTEX-API-AppToken": token,
    "X-VTEX-API-AppKey": key,
    "Cookie": "VtexWorkspace=master%3A-"
}

# Calculando o total de arquivos para a barra de progresso.
total_files = sum([len(os.listdir(template)) for template in template_names if os.path.isdir(template)])

# 3. Para cada template-name:
with tqdm(total=total_files, desc="Processando templates") as pbar:
    for template in template_names:
        folder_path = template
        
        # a. Abrir a pasta com o nome correspondente.
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".json"):
                file_path = os.path.join(folder_path, file_name)
                try:
                    # b. Atualizar o campo email e obter o número da linha.
                    email_lines = update_email_in_file(file_path, email)
                    
                    # c. Ler o arquivo JSON atualizado.
                    with open(file_path, "r") as file:
                        data = json.load(file)
                    
                    # d. Fazer o request para a VTEX utilizando os dados fornecidos.
                    url = f"https://{account}.myvtex.com/api/mail-service/pvt/sendmail?an={account}"
                    payload = {
                        "templateName": template,
                        "jsonData": data
                    }
                    response = requests.post(url, headers=headers, json=payload)
                    print(f"Resposta para o template {template} e arquivo {file_name} (linhas do email: {email_lines}): {response.status_code}")
                
                except json.JSONDecodeError:
                    print(f"Erro ao decodificar o JSON no arquivo {file_name}. Pulando este arquivo.")
                
                except Exception as e:
                    print(f"Erro ao processar o arquivo {file_name}: {e}. Pulando este arquivo.")
                
                finally:
                    # Atualizando a barra de progresso
                    pbar.update(1)
                    
                    # Intervalo de 1200ms
                    time.sleep(1.2)
