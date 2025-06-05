import os
import requests
import numpy as np

MODEL_PLUG_BASE = os.getenv("MODEL_PLUG_URL", "http://model-server-plug:8501/v1/models/plug")
MODEL_LAMPADA_BASE = os.getenv("MODEL_LAMPADA_URL", "http://model-server-lampada:8501/v1/models/lampada")

def get_latest_version(model_base_url):
    try:
        url = model_base_url  # ex: http://model-server-plug:8501/v1/models/plug
        response = requests.get(url)
        response.raise_for_status()
        return str(response.json()["model_version"])
    except Exception:
        return "unknown"


def predict_model(instances, model_base_url, version=None):
    try:
        parsed = [[float(val) for val in row] for row in instances]
        version_path = f"/versions/{version}" if version else ""
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


