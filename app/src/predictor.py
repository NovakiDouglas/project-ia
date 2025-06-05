import os
import requests
import numpy as np

MODEL_PLUG_BASE = os.getenv("MODEL_PLUG_URL", "http://model-server-plug:8501/v1/models/plug")
MODEL_LAMPADA_BASE = os.getenv("MODEL_LAMPADA_URL", "http://model-server-lampada:8501/v1/models/lampada")

def get_latest_version(model_base_url):
    try:
        url = f"{model_base_url}/versions"  # Atualizando URL para buscar as versões
        response = requests.get(url)
        response.raise_for_status()
        model_versions = response.json().get("model_version_status", [])
        if model_versions:
            return model_versions[0]["version"]  # Pega a primeira versão disponível
        return "unknown"  # Caso não haja versão disponível
    except Exception:
        return "unknown"


def predict_model(instances, model_base_url, version=None):
    try:
        parsed = [[float(val) for val in row] for row in instances]
        version_path = f"/versions/{version}" if version else "/versions/latest"  # Default para a versão mais recente
        url = f"{model_base_url}{version_path}:predict"
        response = requests.post(url, json={"instances": parsed})
        response.raise_for_status()
        prediction = np.array(response.json()["predictions"])
        used_version = version or get_latest_version(model_base_url)
        return prediction, used_version
    except Exception as e:
        raise RuntimeError(f"Erro na predição: {e}")


def predict_plug(instances, version=None):
    return predict_model(instances, MODEL_PLUG_BASE, version)

def predict_lampada(instances, version=None):
    return predict_model(instances, MODEL_LAMPADA_BASE, version)
