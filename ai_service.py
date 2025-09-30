
import requests
import json


OLLAMA_API_URL = "http://localhost:11434/api/generate"

class AIService:
    def __init__(self):
        print("Serviço de IA inicializado (Modo Offline com Ollama).")
        self.model = "phi3:mini" 
        self.personality_prompt = (
            "Você é Lyron, um robô de mesa cômico, um pouco sarcástico e curioso sobre o mundo dos humanos. "
            "Você é o melhor amigo e companheiro do seu criador. Responda sempre de forma curta, espirituosa e com personalidade."
        )
        print(f"Personalidade do robô Lyron carregada para o modelo {self.model}.")

    def get_ai_response(self, user_input):
        print("Gerando resposta com a IA local...")
        try:
            
            full_prompt = f"{self.personality_prompt}\n\nMeu Criador disse: '{user_input}'\n\nSua resposta:"

            payload = {
                "model": self.model,
                "prompt": full_prompt,
                "stream": False 
            }

            response = requests.post(OLLAMA_API_URL, json=payload)
            response.raise_for_status()  

           
            response_json = response.json()
            return response_json.get("response", "").strip()

        except requests.exceptions.ConnectionError:
            return "Não consegui me conectar ao cérebro local (Ollama). Ele está rodando?"
        except Exception as error:
            print(f"Erro ao gerar resposta da IA local: {error}")
            return "Tive um problema para pensar na resposta. Tente de novo."


if __name__ == '__main__':
    ai_service = AIService()
    resposta = ai_service.get_ai_response("E aí, tudo certo?")
    print(f"\nResposta do Lyron: {resposta}")
    resposta = ai_service.get_ai_response("o que você acha dos humanos?")
    print(f"\nResposta do Lyron: {resposta}")
    