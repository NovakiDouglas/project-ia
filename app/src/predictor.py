import requests
import numpy as np

def predict_model(instances, model_name, port="8501", version=None):
    try:
        parsed = [[float(val) for val in row] for row in instances]
        version_path = f"/versions/{version}" if version else ""
        url = f"http://{model_name}:{port}/v1/models/{model_name}{version_path}:predict"
        response = requests.post(url, json={"instances": parsed})
        response.raise_for_status()
        return np.array(response.json()["predictions"])
    except Exception as e:
        raise RuntimeError(f"Erro na predição do modelo '{model_name}': {e}")

def predict_plug(instances, version=None):
    return predict_model(instances, model_name="model-lampada-server-plug", port="8501", version=version)

def predict_lampada(instances, version=None):
    return predict_model(instances, model_name="model-lampada-server-lampada", port="8502", version=version)
