import base64
from flask import Flask, jsonify, request
from flask_cors import CORS  # Importar o Flask-CORS
from deepface import DeepFace
from PIL import Image, ImageEnhance
from io import BytesIO
import cv2
import numpy as np

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

# Função para melhorar brilho e contraste e aplicar filtro bilateral
def preprocess_image(image_pil):
    # Ajuste automático de brilho e contraste com PIL
    enhancer_brightness = ImageEnhance.Brightness(image_pil)
    image_pil = enhancer_brightness.enhance(1.2)  # Aumenta um pouco o brilho

    enhancer_contrast = ImageEnhance.Contrast(image_pil)
    image_pil = enhancer_contrast.enhance(1.3)  # Aumenta um pouco o contraste

    # Converter PIL para OpenCV
    image_cv = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)

    # Aplicar filtro bilateral para suavização sem perda de bordas (ótimo para rostos)
    image_cv = cv2.bilateralFilter(image_cv, d=9, sigmaColor=75, sigmaSpace=75)

    # Converter de volta para PIL
    image_rgb = cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB)
    return Image.fromarray(image_rgb)

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

        # Pré-processa a imagem para melhor detecção facial
        image = preprocess_image(image)

        # Salva a imagem temporariamente
        image.save("uploaded_image.jpg") 

        # Analisar emoção com DeepFace
        result = DeepFace.analyze(img_path="uploaded_image.jpg", actions=["emotion"])
        print(result)  # Para inspecionar os dados

        # Convertendo os valores para tipo `float` no dicionário de emoções
        emotions = {key: float(value) for key, value in result[0]['emotion'].items()}
        dominant_emotion = result[0]['dominant_emotion']

        # Obter categoria e valor (0 ou 1)
        emotion_category, emotion_value = emotion_mapping.get(dominant_emotion, ("neutra", 0))

        # Prints de debug
        print(f"Emoção dominante detectada: {dominant_emotion}")
        print(f"Categoria mapeada: {emotion_category}")
        print(f"Valor final (0 ou 1): {emotion_value}")

        return jsonify({'emotion': emotion_value}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

