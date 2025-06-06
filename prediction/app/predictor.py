import os
import requests
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("predictor")

MODEL_PLUG_BASE = os.getenv("MODEL_PLUG_URL", "http://model-server-plug:8501/v1/models/plug")
MODEL_LAMP_BASE = os.getenv("MODEL_LAMP_URL", "http://model-server-lamp:8501/v1/models/lamp")
# Fator oficial de emissão (MCTI, 2024): 42.6 kg CO₂ por MWh
EMISSION_FACTOR_KG_PER_MWH = 42.6

def get_latest_version(model_base_url):
    try:
        url = f"{model_base_url}/versions"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        model_versions = response.json().get("model_version_status", [])
        if model_versions and isinstance(model_versions, list):
            return model_versions[0].get("version", "unknown")
        return "unknown"
    except Exception as e:
        logger.error(f"Error fetching version for {model_base_url}: {e}")
        return "unknown"



def predict_model(instances, model_base_url, version=None):
    try:
        parsed = [[float(val) for val in row] for row in instances]
        version_path = f"/versions/{version}" if version else "/versions/latest"
        url = f"{model_base_url}{version_path}:predict"
        response = requests.post(url, json={"instances": parsed}, timeout=10)
        response.raise_for_status()

        prediction = np.array(response.json()["predictions"]).flatten()
        used_version = version or get_latest_version(model_base_url)

        # ⚡ Calcula pegada de carbono para cada previsão (assume valor em MWh)
        carbon_footprint = [round(value * EMISSION_FACTOR_KG_PER_MWH, 3) for value in prediction]

        return prediction.tolist(), carbon_footprint, used_version
    except Exception as e:
        logging.error(f"Erro na predição com o modelo {model_base_url}: {e}")
        raise RuntimeError(f"Erro na predição: {e}")

def predict_plug(instances, version=None):
    return predict_model(instances, MODEL_PLUG_BASE, version)

def predict_lamp(instances, version=None):
    return predict_model(instances, MODEL_LAMP_BASE, version)