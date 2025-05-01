# 🧠 API de Detecção de Emoções

## 📌 Descrição

Este projeto é parte do Trabalho de Conclusão de Curso (TCC) e representa a **camada de API** desenvolvida em Python com Flask. A API utiliza a biblioteca **DeepFace** para identificar emoções humanas a partir de imagens enviadas no formato Base64. Como resposta, a API retorna uma classificação emocional **simplificada** (positiva ou negativa), permitindo fácil integração com interfaces visuais ou outras aplicações.

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

   Ative o ambiente virtual:

   ```bash
   .\venv\Scripts\activate
   ```

   O prompt deve mudar para `(venv) PS C:\Users\SeuUsuario\TCC>`.

4. **Instale as Dependências**:

   - Com o ambiente virtual ativado, instale as bibliotecas necessárias:

     ```bash
     pip install flask flask-cors deepface numpy pillow opencv-python
     ```

   - Ou utilize o arquivo `requirements.txt` para instalar as versões exatas utilizadas no projeto (recomendado):

     ```bash
     pip install -r requirements.txt
     ```

   - Isso instalará:
     - `flask`: Framework para criação da API e integração com o front-end.
     - `flask-cors`: Suporte a requisições CORS para comunicação com o front-end.
     - `deepface`: Detecção de emoções em imagens.
     - `numpy`: Manipulação de arrays para processamento de imagens.
     - `pillow`: Manipulação de imagens no formato PIL.
     - `opencv-python`: Captura e processamento de imagens/vídeos.
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
     ```

   - Salve como `test_libs.py` e execute:

     ```bash
     python test_libs.py
     ```

   - Se não houver erros, a instalação foi bem-sucedida.

6. **Execute a API**:

   - Inicie a API:

     ```bash
     python app.py
     ```

## 🚀 Após executar a API com sucesso, siga para o front-end.

## 🎯 Objetivo Geral do Projeto

Capturar imagens da webcam do usuário, detectar a emoção dominante utilizando Inteligência Artificial (DeepFace) e adaptar dinamicamente a interface do usuário de acordo com a emoção predominante (positiva ou negativa).

## 🔍 Detalhes da API

A API foi desenvolvida utilizando o **Flask**, um microframework leve e flexível em Python, ideal para projetos que requerem rapidez no desenvolvimento e integração com front-ends. O Flask foi escolhido por sua **simplicidade**, **facilidade de configuração** e **capacidade de integração com bibliotecas de IA**, como o DeepFace, além de ser amplamente utilizado em aplicações web e APIs RESTful. Sua arquitetura minimalista permitiu focar na lógica de detecção de emoções sem a complexidade de frameworks mais robustos, tornando-o perfeito para o escopo do TCC, que exige uma API eficiente e de fácil manutenção.

### Funcionalidades Principais:
- **Recebimento de Imagens**: Aceita até **100 imagens** codificadas em Base64 via requisições POST no endpoint `/api/analyze_emotion`, enviadas como um array JSON (`{"images": ["base64_1", "base64_2", ...]}`).
- **Pré-processamento**: Aplica ajustes de brilho e contraste com a biblioteca Pillow e filtro bilateral com OpenCV para melhorar a detecção facial.
- **Análise de Emoções**: Utiliza o **DeepFace** para detectar a emoção dominante em cada imagem, retornando probabilidades para emoções como "happy", "sad", "angry", etc.
- **Anotação e Salvamento**: Anota a emoção dominante na imagem (e.g., "Emotion: happy") e salva cada frame como `image_<index>.png` (e.g., `image_1.png`, `image_2.png`, ..., `image_100.png`) na pasta `output_images`, sobrescrevendo arquivos existentes com os mesmos nomes em novas execuções.
- **Resposta da API**: Retorna uma lista de resultados para todos os frames, incluindo:
  - `frame`: Número do frame (1 a 100).
  - `emotion`: Valor simplificado (0 para positiva/neutra, 1 para negativa).
  - `dominant_emotion`: Emoção detectada (e.g., "happy", "sad").
  - `category`: Categoria da emoção (e.g., "positiva", "negativa").
- **Tratamento de Erros**: Lida com erros por frame (e.g., Base64 inválido) sem interromper o processamento, retornando mensagens de erro específicas.

### Motivos para Escolher o Flask:
- **Simplicidade e Leveza**: O Flask é um microframework que oferece apenas o essencial para criar APIs, permitindo configurar rapidamente endpoints como `/api/analyze_emotion` sem overhead desnecessário.
- **Flexibilidade**: Facilita a integração com bibliotecas como DeepFace, Pillow e OpenCV, que são centrais para o processamento de imagens e análise de emoções.
- **Comunidade e Documentação**: Possui uma vasta comunidade e documentação abrangente, o que agilizou o desenvolvimento e a resolução de problemas durante o TCC.
- **Adequação ao Escopo**: Para um projeto acadêmico como o TCC, que requer uma API focada em funcionalidades específicas (detecção de emoções e integração com front-end), o Flask é ideal por sua curva de aprendizado curta e facilidade de manutenção.
- **Suporte a CORS**: Com o pacote `flask-cors`, a API suporta requisições cross-origin, essencial para comunicação com o front-end hospedado em um repositório separado.

### Atualizações Recentes:
- **Suporte a Múltiplos Frames**: Anteriormente, a API processava uma única imagem por requisição, salvando-a como `image_1.png`. Agora, suporta até **100 frames** em uma única requisição, permitindo o processamento em lote de imagens (e.g., frames de vídeo capturados pela webcam).
- **Nomenclatura Dinâmica**: Cada frame é salvo com um nome único (`image_1.png` a `image_100.png`), com sobrescrita de arquivos existentes em novas execuções, atendendo ao requisito de reutilização de nomes.
- **Resposta Aprimorada**: A API agora retorna uma lista de resultados detalhados para todos os frames processados, em vez de um único valor de emoção.
- **Robustez**: Adicionado tratamento de erros por frame, garantindo que falhas em uma imagem não interrompam o processamento das demais.
- **Limite de Frames**: Implementado um limite de 100 frames (`MAX_FRAMES = 100`) para evitar sobrecarga no servidor.
- **Logs Detalhados**: Incluídos logs específicos por frame para facilitar a depuração durante o desenvolvimento.

### Por Que Essas Alterações?
As modificações foram feitas para atender à necessidade de processar múltiplas imagens capturadas pela webcam, como em um fluxo de vídeo ou uma sequência de fotos, permitindo uma análise mais dinâmica e em tempo real das emoções do usuário. O suporte a 100 frames alinha-se com o objetivo de adaptar a interface do front-end com base em uma sequência de emoções detectadas, enquanto a sobrescrita de arquivos mantém a organização da pasta `output_images`. O Flask foi mantido como base por sua capacidade de suportar essas mudanças sem comprometer a simplicidade do projeto.

---
```

1. **Atualização da Seção "Detalhes da API"**:
   - **Adicionada Explicação do Flask**:
     - Descrito o que é o Flask (microframework leve e flexível).
     - Explicado por que é bom: simplicidade, flexibilidade, suporte a bibliotecas de IA, comunidade forte e adequação a projetos acadêmicos.
     - Justificado a escolha: ideal para o TCC devido à curva de aprendizado curta, integração com DeepFace e suporte a CORS para o front-end.
   - **Incorporadas as Modificações**:
     - Detalhado o suporte a 100 frames, com entrada via array JSON.
     - Explicado o salvamento de imagens com nomes dinâmicos (`image_<index>.png`) e sobrescrita.
     - Descrita a nova resposta da API (lista de resultados por frame).
     - Mencionado o tratamento de erros por frame e o limite de `MAX_FRAMES`.
     - Incluídos logs detalhados para depuração.
   - **Motivo das Alterações**:
     - Explicado que as mudanças permitem processar sequências de imagens (e.g., frames de vídeo), alinhando-se com o objetivo de adaptar a interface do front-end dinamicamente.
     - Reforçado que o Flask suporta essas mudanças sem adicionar complexidade.

2. **Manutenção do Estilo**:
   - Mantido o tom e a formatação do README original, com emojis (🧠, 🔍, etc.) e linguagem acessível.
   - Adicionados detalhes técnicos sem comprometer a clareza para leitores não técnicos.

3. **Atualização das Dependências**:
   - Incluído `flask-cors` na lista de dependências instaladas, já que é usado no código para suportar requisições cross-origin.
   - Mantida a menção a `requirements.txt` para instalação de versões exatas.

### Como Usar no Projeto

1. **Atualizar o README**:
   - Substitua o conteúdo do arquivo `README.md` no repositório `TCC-API` pelo texto acima.
   - Alternativamente, adicione apenas a seção atualizada **🔍 Detalhes da API** ao seu README existente, mesclando com o conteúdo atual.

2. **Commit das Alterações**:
   - Use a mensagem de commit sugerida anteriormente para documentar as mudanças no código e no README:
     ```bash
     git add main.py README.md
     git commit -m "Adiciona suporte para processamento de até 100 frames de imagens em /api/analyze_emotion" -m "- Modifica endpoint para aceitar array JSON de imagens Base64." -m "- Processa e salva cada frame como image_<index>.png com sobrescrita." -m "- Retorna lista de resultados de emoções para todos os frames." -m "- Implementa tratamento de erros por frame e limite de 100 frames." -m "- Usa arquivos temporários únicos por frame para análise do DeepFace." -m "- Atualiza README com detalhes das mudanças e justificativa para uso do Flask."
     git push origin main
     ```

3. **Verificar no Repositório**:
   - Acesse `https://github.com/davisbalbino/TCC-API` e confirme que o README reflete as mudanças.
   - Teste a API com o front-end para garantir integração.

### Justificativa para o Flask (Resumida)

- **Por que é bom?**:
  - **Leveza**: O Flask é minimalista, exigindo menos configuração que frameworks como Django, o que acelera o desenvolvimento.
  - **Flexibilidade**: Permite integrar bibliotecas específicas (DeepFace, OpenCV, Pillow) sem impor estruturas rígidas.
  - **Integração com Front-end**: Com `flask-cors`, suporta requisições cross-origin, essencial para o front-end em um repositório separado.
  - **Comunidade**: Ampla documentação e suporte comunitário facilitam a resolução de problemas.

- **Por que escolhemos?**:
  - Para o TCC, o foco era criar uma API funcional e integrada com o front-end, sem complexidade desnecessária.
  - O Flask permitiu implementar rapidamente o endpoint `/api/analyze_emotion`, integrar o DeepFace e adicionar suporte a 100 frames, mantendo o código simples e manutenível.
  - Sua adequação a projetos acadêmicos e facilidade de aprendizado foram decisivas para a equipe.

### Testando as Alterações

1. **Instale Dependências**:
   ```bash
   pip install flask flask-cors deepface numpy pillow opencv-python
   ```

2. **Execute a API**:
   ```bash
   python main.py
   ```

3. **Teste o Endpoint**:
   - Envie uma requisição POST com um array JSON de imagens Base64:
     ```bash
     curl -X POST -H "Content-Type: application/json" -d '{"images":["base64_1","base64_2"]}' http://localhost:5000/api/analyze_emotion
     ```
   - Verifique a pasta `output_images` para `image_1.png`, `image_2.png`, etc.
   - Confirme que a resposta contém resultados para todos os frames:
     ```json
     {
         "results": [
             {"frame": 1, "emotion": 0, "dominant_emotion": "happy", "category": "positiva"},
             {"frame": 2, "emotion": 1, "dominant_emotion": "sad", "category": "negativa"}
         ]
     }
     ```
4. **Teste com o Front-end**:
   - Siga as instruções no repositório `TCC-FRONT` para executar o front-end.
   - Certifique-se de que a webcam está capturando imagens e enviando-as como um array JSON para a API.

