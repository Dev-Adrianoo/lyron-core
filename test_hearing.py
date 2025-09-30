from audio_service import AudioService

def main():
  print("--- Iniciando teste do serviço de áudio --- ")
  audio_service = AudioService()

  texto_ouvindo = audio_service.listen()

  if texto_ouvindo:
    print(f"\n SUCESSO! o Serviço de áudio capturou: '{texto_ouvindo} '")
  else:
    print("\nFALHA! O Serviço de áudio não conseguiu captura o texto.")
  
  print("--- Teste do serviço de áudio finalizado ---")

if __name__ == "__main__":
  main()