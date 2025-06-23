import os
import json
import requests
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("predictor")

MODEL_PLUG_BASE = os.getenv(
    "MODEL_PLUG_URL", "http://model-server-plug:8501/v1/models/plug"
)
MODEL_LAMP_BASE = os.getenv(
    "MODEL_LAMP_URL", "http://model-server-lamp:8501/v1/models/lamp"
)

EMISSION_FACTOR_KG_PER_MWH = 42.6

# --- carrega o mapa product_id → indice ---
_map_path = os.path.join(os.path.dirname(__file__), "prod_idx_map.json")
with open(_map_path, "r") as f:
    PROD_IDX_MAP = json.load(f)


def get_latest_version(model_base_url):
    try:
        response = requests.get(model_base_url, timeout=10)
        response.raise_for_status()
        model_info = response.json()
        return model_info.get("model_version_status", [{}])[0].get("version", "unknown")
    except Exception as e:
        logger.error(f"Erro ao buscar versão mais recente de {model_base_url}: {e}")
        return "unknown"


def predict_model(instances, model_base_url, version=None):
    try:
        parsed = [[float(val) for val in row] for row in instances]
        version_path = f"/versions/{version}" if version else ""
        url = f"{model_base_url}{version_path}:predict"

        logger.info(f"Requisição para: {url}")
        response = requests.post(url, json={"instances": parsed}, timeout=10)
        response.raise_for_status()

        prediction = np.array(response.json()["predictions"]).flatten()
        used_version = version or get_latest_version(model_base_url)
        carbon_footprint = [
            round(val * EMISSION_FACTOR_KG_PER_MWH, 3) for val in prediction
        ]

        return prediction.tolist(), carbon_footprint, used_version
    except Exception as e:
        logger.error(f"Erro na predição com o modelo {model_base_url}: {e}")
        raise RuntimeError(f"Erro na predição: {e}")


def predict_plug(instances, version=None):
    return predict_model(instances, MODEL_PLUG_BASE, version)


def predict_lamp(payload_list, version=None):
    """
    payload_list: [
      { "num_input": [...], "product_id": "<bruto>" },
      ...
    ]
    """
    try:
        # 1) converte cada product_id bruto em índice
        instances = []
        for inst in payload_list:
            num_in = inst.get("num_input")
            raw_id = inst.get("product_id")
            idx = PROD_IDX_MAP.get(raw_id)
            if idx is None:
                raise RuntimeError(f"product_id desconhecido: {raw_id}")
            # monta exatamente o JSON que o TF-Serving espera:
            instances.append({
                "num_input": num_in,
                "prod_input": [idx]
            })

        # 2) chama o endpoint de lamp diretamente (sem usar predict_model)
        version_path = f"/versions/{version}" if version else ""
        url = f"{MODEL_LAMP_BASE}{version_path}:predict"
        logger.info(f"Requisição lamp para: {url}")

        resp = requests.post(url, json={"instances": instances}, timeout=10)
        resp.raise_for_status()

        preds = np.array(resp.json()["predictions"]).flatten()
        used_version = version or get_latest_version(MODEL_LAMP_BASE)
        carbon = [round(p * EMISSION_FACTOR_KG_PER_MWH, 3) for p in preds]
        return preds.tolist(), carbon, used_version

    except Exception as e:
        logger.error(f"Erro na predição com o modelo {MODEL_LAMP_BASE}: {e}")
        raise RuntimeError(f"Erro na predição: {e}")
