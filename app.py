import base64
from flask import Flask, jsonify, request
from flask_cors import CORS  # Importar o Flask-CORS
from deepface import DeepFace
from PIL import Image
from io import BytesIO

app = Flask(__name__)
CORS(app)  # Permitir CORS para todos os domínios em todas as rotas


emotion_mapping = {
    "happy": ("positiva", 0),
    "surprise": ("positiva", 0),
    "sad": ("negativa", 1),
    "angry": ("negativa", 1),
    "fear": ("negativa", 1),
    "disgust": ("negativa", 1),
    "neutral": ("positiva", 0)
}


# Rota para receber a imagem e detectar emoções
@app.route('/api/analyze_emotion', methods=['POST'])
def analyze_emotion():
    try:
        # Captura a imagem Base64 do corpo da requisição
        base64_image = request.json.get('image', '')
        if not base64_image:
            return jsonify({'error': 'Imagem Base64 não fornecida!'}), 400

        # Decodifica a imagem Base64
        
        image_data = base64.b64decode(base64_image)
        image = Image.open(BytesIO(image_data))

        # Converter para RGB (remover canal de transparência)
        if image.mode == "RGBA":
            image = image.convert("RGB")

        image.save("uploaded_image.jpg") 

        # Analisar emoção com DeepFace
        
        result = DeepFace.analyze(img_path="uploaded_image.jpg", actions=["emotion"])
        print(result)  # Para inspecionar os dados

        # Convertendo os valores para tipo `float` no dicionário de emoções
        emotions = {key: float(value) for key, value in result[0]['emotion'].items()}
        dominant_emotion = result[0]['dominant_emotion']

        return jsonify({'emotion': emotion_mapping[dominant_emotion]}), 200



        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)