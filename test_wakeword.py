import os
import struct
import pyaudio
import pvporcupine

def teste_wake_word():
  """
  Testa o motor de wake word Porcupine com uma palavra padrão.
  """
  access_key = os.getenv("PICOVOICE_ACCESS_KEY")
  if not access_key:
    print("Chave de acesso para PICOVOICE não encontrada.")
    return
  
  porcupine  = None
  pa = None
  audio_stream = None

  try:
    porcupine = pvporcupine.create(
      access_key =access_key,
      keywords=['porcupine']
    )
    
    pa = pyaudio.PyAudio()
    audio_stream = pa.open(
      rate=porcupine .sample_rate,
      channels=1,
      format=pyaudio.paInt16,
      input=True,
      frames_per_buffer=porcupine.frame_length
    )
    print("O 'Porteiro (Porcupine) está ouvindo...")
    print("Diga 'Porcupine (pronuncia-se 'Pór-kiu-pain') para testar.'")

    while True:
      pcm = audio_stream.read(porcupine.frame_length)
      pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

      keyword_index = porcupine.process(pcm)

      if keyword_index >= 0:
        print(f" Palavra de ativação 'porcupine' detectada!")
  except KeyboardInterrupt:
    print("\nEncerrando o teste de wake word.")      
  except Exception  as e:
    print(f"Ocorreu um erro: {e}")
  finally:
    if porcupine is not None:
      porcupine.delete()
    if audio_stream is not None:
      audio_stream.close()
    if pa is not None:
      pa.terminate()
if __name__ == "__main__":
  teste_wake_word()