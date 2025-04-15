import base64

# Função para converter uma imagem em Base64
def image_to_base64(image_path):
    try:
        # Abrir a imagem em modo binário
        with open(image_path, "rb") as image_file:
            # Codificar a imagem em Base64
            base64_string = base64.b64encode(image_file.read()).decode('utf-8')
            return base64_string
    except Exception as e:
        return f"Erro: {e}"

# Exemplo de uso
image_path = "pessoafeliz.jpg"  # Substitua pelo caminho da sua imagem
base64_result = image_to_base64(image_path)
print(base64_result)  # Exibe o resultado Base64