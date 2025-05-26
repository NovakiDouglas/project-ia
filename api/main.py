
from flask import Flask, request, jsonify,abort

app = Flask(__name__)

@app.route('/predict', methods=['GET'])
def predict():
    id = request.args.get('id')
    if not id:
        abort(400, description="id is required")
    return jsonify({'success': True, 'id': id})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
