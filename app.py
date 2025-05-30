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

# Mesma coisa só que para imagem sem o filtro
OUTPUT_FOLDER_NO_FILTER = "output_images_no_filter"
if not os.path.exists(OUTPUT_FOLDER_NO_FILTER):
    os.makedirs(OUTPUT_FOLDER_NO_FILTER)

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

        # Contadores de emoções
        positive_count = 0
        negative_count = 0

        # Lista para armazenar resultados individuais
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
                    
                # -------------------------- não interfere (sem filtro)-----------------------------
                
                # Análise da imagem SEM filtro
                no_filter_path = os.path.join(OUTPUT_FOLDER_NO_FILTER, f"image_no_filter_{index}.png")
                image.save(no_filter_path)    
                
                # Detectar emoção sem filtro
                result_no_filter = DeepFace.analyze(img_path=no_filter_path, actions=["emotion"], enforce_detection=False)
                dominant_emotion_no_filter = result_no_filter[0]['dominant_emotion']
                
                # Anotar a imagem sem filtro
                image_cv_no_filter = cv2.imread(no_filter_path)
                cv2.putText(image_cv_no_filter, f"Emotion: {dominant_emotion_no_filter}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)  # Cor vermelha
                cv2.imwrite(no_filter_path, image_cv_no_filter)
                print(f"Saved annotated image without filter: {no_filter_path}")    
                
                # -------------------------- não interfere (sem filtro) -----------------------------           

                # Pré-processa a imagem para melhor detecção facial
                filtered_image = preprocess_image(image)

                # Salva a imagem temporariamente para DeepFace
                temp_image_path = os.path.join(OUTPUT_FOLDER, f"temp_image_{index}.jpg")
                filtered_image.save(temp_image_path)

                # Analisar emoção com DeepFace
                result = DeepFace.analyze(img_path=temp_image_path, actions=["emotion"], enforce_detection=False)
                dominant_emotion = result[0]['dominant_emotion']
                
                # Obter categoria e valor (0 ou 1)
                emotion_category, emotion_value = emotion_mapping.get(dominant_emotion, ("neutra", 0))
                
                # Carregar a imagem com OpenCV
                image_cv = cv2.imread(temp_image_path)

                # Anotar a imagem com a emoção detectada
                cv2.putText(image_cv, f"Emotion: {dominant_emotion}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2) # VERDE

                # Salvar a imagem anotada na pasta
                output_path = os.path.join(OUTPUT_FOLDER, f"image_{index}.png")
                cv2.imwrite(output_path, image_cv)
                print(f"Saved annotated image with filter: {output_path}")

                # Contabilizar emoções
                if emotion_value == 0:
                    positive_count += 1
                else:
                    negative_count += 1

                # Adicionar resultado da imagem COM filtro (resposta da API)
                results.append({
                    'frame': index,
                    'emotion': emotion_value,
                    'dominant_emotion': dominant_emotion,
                    'category': emotion_category
                })

                # Remover a imagem temporária
                os.remove(temp_image_path)

            except Exception as e:
                results.append({
                    'frame': index,
                    'error': f"Erro ao processar frame: {str(e)}"
                })

        # Determinar qual emoção teve maior ocorrência
        final_emotion_value = 0 if positive_count >= negative_count else 1
        final_dominant_emotion = "Positivo" if final_emotion_value == 0 else "Negativo"
        print (final_dominant_emotion)

        return jsonify({
            'results': results,
            'emotion': final_emotion_value,  # Mantém o formato esperado (0 ou 1)
            'dominant_emotion': final_dominant_emotion,
            'category': "positiva" if final_emotion_value == 0 else "negativa"
        }), 200

    except Exception as e:
        return jsonify({'error': f"Erro geral: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)