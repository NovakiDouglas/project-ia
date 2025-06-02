import os
import requests
import numpy as np

MODEL_PLUG_BASE = os.getenv("MODEL_PLUG_URL", "http://model-server-plug:8501/v1/models/plug")
MODEL_LAMPADA_BASE = os.getenv("MODEL_LAMPADA_URL", "http://model-server-lampada:8501/v1/models/lampada")

def predict_model(instances, model_base_url, version=None):
    try:
        parsed = [[float(val) for val in row] for row in instances]
        version_path = f"/versions/{version}" if version else ""
        url = f"{model_base_url}{version_path}:predict"
        response = requests.post(url, json={"instances": parsed})
        response.raise_for_status()
        return np.array(response.json()["predictions"])
    except Exception as e:
        raise RuntimeError(f"Erro na predição: {e}")

def predict_plug(instances, version=None):
    return predict_model(instances, MODEL_PLUG_BASE, version)

def predict_lampada(instances, version=None):
    return predict_model(instances, MODEL_LAMPADA_BASE, version)
