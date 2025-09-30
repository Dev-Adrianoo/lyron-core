from ai_service import AIService

def main():
  print("--- Iniciando teste do serviço de IA ---")
  ai_service = AIService()

  pergunta = "E aí, tudo bem? Oque você acha sobre programação"
  print(f"\nEnviando pergunta: '{pergunta}'")

  resposta_ia = ai_service.get_ai_response(pergunta)

  print("\n--- RESPOSTA DA IA ---")
  print(resposta_ia)
  print("------------------------------------")


if __name__ == "__main__":
  main()