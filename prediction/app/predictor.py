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
        url = f"{model_base_url}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        model_info = response.json()
        return model_info.get("model_version_status", [{}])[0].get("version", "unknown")
    except Exception as e:
        logger.error(f"Erro ao buscar versão mais recente de {model_base_url}: {e}")
        return "unknown"

def predict_model(instances, model_base_url, version=None):
    try:
        # Formatação compatível com REST API do TensorFlow Serving
        parsed = [[float(val) for val in row] for row in instances]
        version_path = f"/versions/{version}" if version else ""
        url = f"{model_base_url}{version_path}:predict"

        logger.info(f"Requisição para: {url}")
        response = requests.post(url, json={"instances": parsed}, timeout=10)
        response.raise_for_status()

        prediction = np.array(response.json()["predictions"]).flatten()
        used_version = version or get_latest_version(model_base_url)

        carbon_footprint = [round(val * EMISSION_FACTOR_KG_PER_MWH, 3) for val in prediction]

        return prediction.tolist(), carbon_footprint, used_version
    except Exception as e:
        logger.error(f"Erro na predição com o modelo {model_base_url}: {e}")
        raise RuntimeError(f"Erro na predição: {e}")

def predict_plug(instances, version=None):
    return predict_model(instances, MODEL_PLUG_BASE, version)

def predict_lamp(payload_list, version=None):
    try:
        # 1) Converter cada valor para float
        parsed = [[float(val) for val in row] for row in payload_list]

        # 2) Separar num_feats (todas as colunas menos a última) e prod_id (última coluna)
        num_feats = [row[:-1] for row in parsed]
        prod_ids  = [int(row[-1]) for row in parsed]

        # 3) Montar URL de predição, possivelmente incluindo versão
        version_path = f"/versions/{version}" if version else ""
        url = f"{MODEL_LAMP_BASE}{version_path}:predict"
        logger.info(f"Requisição para: {url}")

        # 4) Enviar JSON com dois tensores nomeados ("inputs")
        payload = {
            "inputs": {
                "num_feats": num_feats,
                "prod_id":   prod_ids
            }
        }
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()

        # 5) Extrair previsões e calcular pegada de carbono
        prediction = np.array(response.json()["predictions"]).flatten()
        used_version = version or get_latest_version(MODEL_LAMP_BASE)
        carbon_footprint = [
            round(val * EMISSION_FACTOR_KG_PER_MWH, 3)
            for val in prediction
        ]

        return prediction.tolist(), carbon_footprint, used_version

    except Exception as e:
        logger.error(f"Erro na predição com o modelo {MODEL_LAMP_BASE}: {e}")
        raise RuntimeError(f"Erro na predição: {e}")




