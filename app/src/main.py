from flask import Flask, request, jsonify, abort
from predictor import load_model, predict_with_model

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    version = request.args.get('version', 'v1')  # suporte opcional para versão

    try:
        content = request.get_json()
        if not content or 'instances' not in content:
            abort(400, description="O JSON precisa conter a chave 'instances'.")

        instances = content['instances']
        model = load_model(version)
        if model is None:
            return jsonify({'success': False, 'error': f'Modelo versão {version} não encontrado'}), 503

        result = predict_with_model(model, instances)
        return jsonify({'success': True, 'prediction': result.tolist(), 'version': version})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
