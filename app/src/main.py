from flask import Flask, request, jsonify, abort
from predictor import load_model, predict_with_model

app = Flask(__name__)

@app.route('/predict', methods=['GET'])
def predict():
    id = request.args.get('id')
    version = request.args.get('version', 'v1')  # Default para v1

    if not id:
        abort(400, description="id is required")

    model = load_model(version)
    if model is None:
        return jsonify({'success': False, 'error': f'Modelo versão {version} não encontrado'}), 503

    result = predict_with_model(model, id)

    return jsonify({'success': True, 'prediction': result.tolist(), 'version': version})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
