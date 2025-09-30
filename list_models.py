# list_models.py
import os
import google.generativeai as genai

print("Iniciando a listagem de modelos...")

try:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("A chave GOOGLE_API_KEY não foi encontrada.")
    
    genai.configure(api_key=api_key)
    
    print("\nModelos disponíveis que suportam 'generateContent':")
    
    count = 0
    # Itera sobre todos os modelos disponíveis
    for model in genai.list_models():
        # Verifica se o método 'generateContent' está na lista de métodos suportados
        if 'generateContent' in model.supported_generation_methods:
            print(f"- {model.name}")
            count += 1
            
    if count == 0:
        print("Nenhum modelo compatível encontrado. Verifique sua chave de API e permissões.")

except Exception as e:
    print(f"\nERRO ao listar modelos: {e}")