import requests
import os
import numpy as np

MODEL_URL = os.getenv("MODEL_URL", "http://localhost:8501/v1/models/model:predict")

def load_model(version='v1'):
    return True  # Sem carregamento local, container separado cuida disso

def predict_with_model(_, instances):
    try:
        parsed_instances = [[float(val) for val in row] for row in instances]
        response = requests.post(MODEL_URL, json={"instances": parsed_instances})
        response.raise_for_status()
        prediction = response.json()["predictions"]
        return np.array(prediction)
    except Exception as e:
        raise RuntimeError(f"Erro ao obter predição: {e}")
