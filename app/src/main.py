import os
import boto3
import json
from datetime import datetime, timedelta, timezone
from flask import Flask, request, jsonify, abort
from predictor import predict_plug, predict_lampada

app = Flask(__name__)

# Ambiente (dev, prod)
ENV = os.getenv("ENV", "dev")
SECRET_NAME = f"api_key_rotation-{ENV}"
REGION_NAME = os.getenv("AWS_REGION", "us-east-1")

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

def require_api_key():
    api_key = request.headers.get("X-API-KEY")
    if not api_key or not is_valid_key(api_key):
        abort(401, description="Chave de API inválida ou ausente")

@app.route('/predict/plug', methods=['POST'])
def predict_endpoint_plug():
    require_api_key()
    version = request.args.get('version')
    try:
        content = request.get_json()
        if not content or 'instances' not in content:
            abort(400, description="JSON precisa conter a chave 'instances'.")
        instances = content['instances']
        result, used_version = predict_plug(instances, version)
        return jsonify({
            'success': True,
            'prediction': result.tolist(),
            'version': used_version
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/predict/lampada', methods=['POST'])
def predict_endpoint_lampada():
    require_api_key()
    version = request.args.get('version')
    try:
        content = request.get_json()
        if not content or 'instances' not in content:
            abort(400, description="JSON precisa conter a chave 'instances'.")
        instances = content['instances']
        result, used_version = predict_lampada(instances, version)
        return jsonify({
            'success': True,
            'prediction': result.tolist(),
            'version': used_version
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)