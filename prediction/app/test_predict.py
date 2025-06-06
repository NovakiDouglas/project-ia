import requests
import json

# ✅ URL base da API (alterada para porta 8000)
API_URL = "http://54.225.136.207:8000"  # Altere aqui se necessário

# ✅ API Key atual (pode vir do Secrets Manager no projeto principal)
API_KEY = "r_VScYSlXJ2dyIweTahbHg0RC-kKtzOqEx5PnFgQP14"

def test_predict(endpoint: str, instances, version=None):
    # Construindo a URL do endpoint, incluindo versão se necessário
    url = f"{API_URL}/predict/{endpoint}"
    if version:
        url += f"?version={version}"

    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": API_KEY
    }

    payload = {
        "instances": instances
    }

    try:
        # Envia a requisição POST para a API
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Levanta erro para status HTTP >= 400
        result = response.json()  # Converte a resposta para JSON
        print(f"\n✅ {endpoint.upper()} - versão: {version or 'latest'}")
        print(json.dumps(result, indent=2))  # Exibe os resultados de forma legível
    except requests.exceptions.HTTPError as e:
        print(f"\n❌ ERRO ({endpoint.upper()} - versão {version or 'latest'}):")
        print(f"Status: {response.status_code}")
        print(response.text)
    except Exception as e:
        print(f"\n❌ ERRO inesperado: {e}")

if __name__ == "__main__":
    # Testes para o modelo 'plug'
    instances_plug = [
        [2, 123.4, 110.0, 15.2],
        [5, 130.0, 129.0, 8.3]
    ]

    test_predict("plug", instances_plug)            # última versão
    test_predict("plug", instances_plug, version=1)
    test_predict("plug", instances_plug, version=2)
    test_predict("plug", instances_plug, version=3)

    # Testes para o modelo 'lampada'
    instances_lampada = [
        [1, 45.3, 40.0, 5.1],
        [3, 60.0, 55.0, 8.2]
    ]

    test_predict("lampada", instances_lampada)      # última versão
    test_predict("lampada", instances_lampada, version=1)
    test_predict("lampada", instances_lampada, version=2)
    test_predict("lampada", instances_lampada, version=3)
