import requests

# ✅ Configuração da API
API_URL = "http://54.235.184.185:8000"
API_KEY = "r_VScYSlXJ2dyIweTahbHg0RC-kKtzOqEx5PnFgQP14"

# 🔧 Defina aqui o modelo e a versão a serem testados
ENDPOINT = "plug"     # ou "lamp"
VERSION = 1         # ou None para latest

# 🔌 Entrada para o modelo de plug
instances_plug = [
    [2, 123.4, 110.0, 15.2],
    [6, 1.679111, 1.755, 1.030035]
]

# 💡 Entrada para o modelo de lâmpada
instances_lamp = [
    [1, 45.3, 40.0, 5.1],
    [3, 60.0, 55.0, 8.2]
]

def test_predict(endpoint: str, instances, version=None):
    url = f"{API_URL}/predict/{endpoint}"
    # if version:
    #     url += f"?version={version}"

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
        print(result)

        print(f"\n✅ {endpoint.upper()} - versão: {version or 'latest'}")
        predictions = result.get("prediction", [])
        carbon = result.get("carbon_footprint_kg", [])

        for i, (pred, cfp) in enumerate(zip(predictions, carbon)):
            print(f"  Instância {i+1}: Consumo = {pred:.2f} kWh | Pegada de carbono = {cfp:.2f} kg CO₂")

        print(f"🔁 Versão do modelo usada: {result.get('version')}")

    except requests.exceptions.HTTPError:
        print(f"\n❌ ERRO ({endpoint.upper()} - versão {version or 'latest'}):")
        print(f"Status: {response.status_code}")
        print(response.text)
    except Exception as e:
        print(f"\n❌ ERRO inesperado: {e}")


if __name__ == "__main__":
    if ENDPOINT == "plug":
        test_predict("plug", instances_plug, version=VERSION)
    elif ENDPOINT == "lamp":
        test_predict("lamp", instances_lamp, version=VERSION)
    else:
        print("❌ ENDPOINT inválido! Use 'plug' ou 'lamp'.")
