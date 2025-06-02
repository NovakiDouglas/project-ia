import requests
import json

API_URL = "http://54.86.132.187:5000"  # Altere aqui

def test_predict(endpoint: str, instances, version=None):
    url = f"{API_URL}/predict/{endpoint}"
    if version:
        url += f"?version={version}"

    payload = {
        "instances": instances
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        print(f"\n✅ {endpoint.upper()} - versão: {version or 'latest'}")
        print(json.dumps(result, indent=2))
    except requests.exceptions.HTTPError as e:
        print(f"\n❌ ERRO ({endpoint.upper()} - versão {version}):")
        print(f"Status: {response.status_code}")
        print(response.text)
    except Exception as e:
        print(f"\n❌ ERRO inesperado: {e}")

if __name__ == "__main__":
    # Testes para modelo plug
    instances_plug = [
        [2, 123.4, 110.0, 15.2],
        [5, 130.0, 129.0, 8.3]
    ]

    test_predict("plug", instances_plug)            # última versão
    test_predict("plug", instances_plug, version=1)
    test_predict("plug", instances_plug, version=2)

    # Testes para modelo lâmpada
    instances_lampada = [
        [1, 45.3, 40.0, 5.1],
        [3, 60.0, 55.0, 8.2]
    ]

    test_predict("lampada", instances_lampada)      # última versão
    test_predict("lampada", instances_lampada, version=1)
