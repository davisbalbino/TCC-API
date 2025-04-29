
import base64
from flask import Flask, jsonify, request
from flask_cors import CORS
from deepface import DeepFace
from PIL import Image, ImageEnhance
from io import BytesIO
import cv2
import numpy as np
import os

app = Flask(__name__)
CORS(app)  # Permitir CORS para todos os domínios em todas as rotas

# Define the output folder
OUTPUT_FOLDER = "output_images"

# Create the output folder if it doesn't exist
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# Maximum number of frames to process
MAX_FRAMES = 100

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

# Rota para receber múltiplas imagens e detectar emoções
@app.route('/api/analyze_emotion', methods=['POST'])
def analyze_emotion():
    try:
        # Captura a lista de imagens Base64 do corpo da requisição
        data = request.json
        base64_images = data.get('images', [])
        if not base64_images:
            return jsonify({'error': 'Nenhuma imagem Base64 fornecida!'}), 400

        # Verificar se o número de frames excede o limite
        if len(base64_images) > MAX_FRAMES:
            return jsonify({'error': f'Número de frames excede o limite de {MAX_FRAMES}!'}), 400

        # Lista para armazenar resultados
        results = []

        # Processar cada imagem
        for index, base64_image in enumerate(base64_images, start=1):
            try:
                # Decodifica a imagem Base64
                image_data = base64.b64decode(base64_image)
                image = Image.open(BytesIO(image_data))

                # Converter para RGB (remover canal de transparência)
                if image.mode == "RGBA":
                    image = image.convert("RGB")

                # Pré-processa a imagem para melhor detecção facial
                image = preprocess_image(image)

                # Salva a imagem temporariamente para DeepFace
                temp_image_path = os.path.join(OUTPUT_FOLDER, f"temp_image_{index}.jpg")
                image.save(temp_image_path)

                # Analisar emoção com DeepFace
                result = DeepFace.analyze(img_path=temp_image_path, actions=["emotion"], enforce_detection=False)
                print(f"Frame {index}: {result}")  # Para inspecionar os dados

                # Convertendo os valores para tipo `float` no dicionário de emoções
                emotions = {key: float(value) for key, value in result[0]['emotion'].items()}
                dominant_emotion = result[0]['dominant_emotion']

                # Obter categoria e valor (0 ou 1)
                emotion_category, emotion_value = emotion_mapping.get(dominant_emotion, ("neutra", 0))

                # Anotar a imagem com a emoção dominante
                image_cv = cv2.imread(temp_image_path)
                cv2.putText(image_cv, f"Emotion: {dominant_emotion}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                # Salvar a imagem anotada com nome único
                output_path = os.path.join(OUTPUT_FOLDER, f"image_{index}.png")
                cv2.imwrite(output_path, image_cv)
                print(f"Saved annotated image: {output_path}")

                # Remover a imagem temporária
                os.remove(temp_image_path)

                # Adicionar resultado à lista
                results.append({
                    'frame': index,
                    'emotion': emotion_value,
                    'dominant_emotion': dominant_emotion,
                    'category': emotion_category
                })

                # Prints de debug
                print(f"Frame {index} - Emoção dominante detectada: {dominant_emotion}")
                print(f"Frame {index} - Categoria mapeada: {emotion_category}")
                print(f"Frame {index} - Valor final (0 ou 1): {emotion_value}")

            except Exception as e:
                # Continuar com o próximo frame em caso de erro
                print(f"Erro ao processar frame {index}: {str(e)}")
                results.append({
                    'frame': index,
                    'error': f"Erro ao processar frame: {str(e)}"
                })

        return jsonify({'results': results}), 200

    except Exception as e:
        return jsonify({'error': f"Erro geral: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
