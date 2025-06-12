# Use uma imagem oficial do Python (escolha uma versão compatível)
FROM python:3.10-slim

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Instalar pacotes essenciais para OpenCV e DeepFace
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0

# Copiar os arquivos necessários para dentro do container
COPY requirements.txt .

# Criar um ambiente virtual e instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código-fonte do projeto
COPY . .

# Definir variáveis de ambiente (opcional)
ENV TF_ENABLE_ONEDNN_OPTS=0

# Expor a porta que o Flask usa
EXPOSE 8000

# Definir o comando de execução do container
CMD ["python", "app.py"]