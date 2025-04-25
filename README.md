# 🧠 API de Detecção de Emoções

## 📌 Descrição

Este projeto é parte do Trabalho de Conclusão de Curso (TCC), e representa a **camada de API** desenvolvida em Python com Flask. A API utiliza a biblioteca **DeepFace** para identificar emoções humanas a partir de imagens enviadas no formato Base64. Como resposta, a API retorna uma classificação emocional **simplificada** (positiva ou negativa), permitindo fácil integração com interfaces visuais ou outras aplicações.

---

## 🚀 Como Executar

Esta API foi projetada para funcionar em conjunto com um **front-end** localizado em outro repositório. Portanto, siga os passos abaixo para executar a API, e depois acesse o front-end:

📎 **Repositório do front-end:**  
[https://github.com/davisbalbino/TCC-FRONT.git](https://github.com/davisbalbino/TCC-FRONT.git)

---

## ✅ Pré-requisitos

- Python 3.8 ou superior (até 3.11)
- Webcam funcional conectada ao computador

---

## ⚙️ Passo a Passo para Instalação (Windows)


1. **Clone o Repositório**:

   - Baixe o projeto ou clone-o usando Git:

     ```bash
     git clone https://github.com/davisbalbino/TCC-API.git
     ```

   - Ou baixe o ZIP e extraia em uma pasta (ex.: `C:\Users\SeuUsuario\TCC`).

2. **Instale o Python (se necessário)**:

   - Verifique se o Python 3.8, 3.9, 3.10 ou 3.11 está instalado:

     ```bash
     python --version
     ```
3. **Crie um Ambiente Virtual (Opcional mas recomendado)**:

   Crie um ambiente virtual para isolar as dependências:

   ```bash
   python -m venv venv
   ```

   Ativo ou ambiente virtual:

   ```bash
   .\venv\Scripts\activate
   ```

   O prompt deve mudar para `(venv) PS C:\Users\SeuUsuario\TCC>`.

4. **Instale as Dependências**:

   - Com o ambiente virtual ativado, instale as bibliotecas necessárias:

     ```bash
     pip install flask deepface numpy Pillow opencv-python
     ```

   - Ou utilize o arquivo `requirements.txt`. Dessa forma, as versões exatas utilizadas no projeto serão instaladas (recomendado):

     ```bash
     pip install -r requirements.txt
     ```  

   - Isso instalará:

     - `opencv-python`: Captura de vídeo e imagens.
     - `deepface`: Detecção de emoções.
     - `flask`: Para integração do Front com a API .
     - `tensorflow/keras`: Backend necessário para DeepFace.

5. **Verifique a Instalação (Opcional)**:

   - Teste se as bibliotecas foram instaladas corretamente:

     ```python
     from flask import Flask
     from deepface import DeepFace
     import numpy as np
     import cv2
     from PIL import Image
     print("Todas as bibliotecas estão instaladas corretamente!")
     print("Todas as bibliotecas estão instaladas!")
     ```

   - Salve como `test_libs.py` e execute:

     ```bash
     python test_libs.py
     ```

   - Se não houver erros, a instalação foi bem-sucedida.

5. **Execute a API**:

   - Com tudo funcionando, inicie o sistema:

     ```bash
     python app.py
     ```

## 🚀 Com o execução da API, dando certo agora vai para o front-end.

## 🎯 Objetivo geral do projeto:
- Capturar imagens da webcam do usuário, detectar a emoção dominante utilizando Inteligência Artificial (DeepFace), e adaptar dinamicamente a interface do usuário de acordo com a emoção predominante (positiva ou negativa). 

## 🔍 Detalhes da API
- Recebe uma imagem em base64 via POST
- Decodifica e salva a imagem
- Analisa com DeepFace para detectar emoções
- Retorna um valor:
- 0 para emoções positivas (happy, surprise, neutral)
- 1 para negativas (sad, angry, fear, disgust)