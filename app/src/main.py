from flask import Flask, request, jsonify, abort
from predictor import predict_plug, predict_lampada

app = Flask(__name__)

@app.route('/predict/plug', methods=['POST'])
def predict_endpoint_plug():
    version = request.args.get('version')
    try:
        content = request.get_json()
        if not content or 'instances' not in content:
            abort(400, description="JSON precisa conter a chave 'instances'.")
        instances = content['instances']
        result = predict_plug(instances, version)
        return jsonify({'success': True, 'prediction': result.tolist(), 'version': version or 'latest'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/predict/lampada', methods=['POST'])
def predict_endpoint_lampada():
    version = request.args.get('version')
    try:
        content = request.get_json()
        if not content or 'instances' not in content:
            abort(400, description="JSON precisa conter a chave 'instances'.")
        instances = content['instances']
        result = predict_lampada(instances, version)
        return jsonify({'success': True, 'prediction': result.tolist(), 'version': version or 'latest'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
