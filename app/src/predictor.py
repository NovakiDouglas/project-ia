import joblib
import os

def load_model(version='v1'):
    model_path = f"models/{version}/modelo.pkl"
    if os.path.exists(model_path):
        return joblib.load(model_path)
    else:
        return None

def predict_with_model(model, input_value):
    # Ajuste: usa float para suportar valores mais gerais
    return model.predict([[float(input_value)]])
