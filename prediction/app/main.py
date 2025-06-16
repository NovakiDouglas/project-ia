import os
import boto3
import json
import logging
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from predictor import predict_plug
from predictor import predict_lamp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("predictor-api")

ENV = os.getenv("ENV", "dev")
SECRET_NAME = f"api_key_rotation-{ENV}"
REGION_NAME = os.getenv("AWS_REGION", "sa-east-1")

app = FastAPI()

class PredictionRequest(BaseModel):
    instances: list

class SingleLampInstance(BaseModel):
    num_feats: list[float]
    prod_id: int

class LampPredictionRequest(BaseModel):
    instances: list

def get_api_keys():
    client = boto3.client("secretsmanager", region_name=REGION_NAME)
    response = client.get_secret_value(SecretId=SECRET_NAME)
    return json.loads(response["SecretString"])

def is_valid_key(key: str) -> bool:
    secret = get_api_keys()
    now = datetime.now(timezone.utc)

    if key == secret.get("current"):
        return True

    if key == secret.get("previous"):
        last_rotation = datetime.fromisoformat(secret["last_rotation"].replace("Z", "+00:00"))
        if now <= last_rotation + timedelta(days=1):
            return True

    return False

def require_api_key(request: Request):
    api_key = request.headers.get("X-API-KEY")
    if not api_key or not is_valid_key(api_key):
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/predict/plug")
async def predict_endpoint_plug(request: Request, content: PredictionRequest, version: str = None):
    require_api_key(request)
    try:
        prediction, carbon_footprint, used_version = predict_plug(content.instances, version)
        return {
            'success': True,
            'prediction': prediction,
            'carbon_footprint_kg': carbon_footprint,
            'version': used_version
        }
    except Exception as e:
        logging.exception("Erro ao processar previsão de plug")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/lamp")
async def predict_endpoint_lamp(request: Request, content: LampPredictionRequest, version: str = None):
    require_api_key(request)
    try:
        # payload = [
        #     inst.num_feats + [inst.prod_id]
        #     for inst in content.instances
        # ]
        payload = content.instances
        prediction, carbon_footprint, used_version = predict_lamp(payload, version)
        return {
            'success': True,
            'prediction': prediction,
            'carbon_footprint_kg': carbon_footprint,
            'version': used_version
        }
    except Exception as e:
        logging.exception("Erro ao processar previsão de lamp")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
