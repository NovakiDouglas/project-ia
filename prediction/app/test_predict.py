import requests
import json

# ✅ Configuração da API
API_URL = "http://3.224.60.7:8000"
API_KEY = "r_VScYSlXJ2dyIweTahbHg0RC-kKtzOqEx5PnFgQP14"

def test_predict(endpoint: str, instances, version=None):
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
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

        print(f"\n✅ {endpoint.upper()} - versão: {version or 'latest'}")
        predictions = result.get("prediction", [])
        carbon = result.get("carbon_footprint", [])

        for i, (pred, cfp) in enumerate(zip(predictions, carbon)):
            print(f"  Instância {i+1}: Consumo = {pred:.2f} kWh | Pegada de carbono = {cfp:.2f} g CO₂")

        print(f"🔁 Versão do modelo usada: {result.get('version')}")

    except requests.exceptions.HTTPError:
        print(f"\n❌ ERRO ({endpoint.upper()} - versão {version or 'latest'}):")
        print(f"Status: {response.status_code}")
        print(response.text)
    except Exception as e:
        print(f"\n❌ ERRO inesperado: {e}")

if __name__ == "__main__":
    instances_plug = [
        [2, 123.4, 110.0, 15.2],
        [5, 130.0, 129.0, 8.3]
    ]

    instances_lampada = [
        [1, 45.3, 40.0, 5.1],
        [3, 60.0, 55.0, 8.2]
    ]

    for v in [None, 1, 2, 3]:
        test_predict("plug", instances_plug, version=v)
        test_predict("lampada", instances_lampada, version=v)
