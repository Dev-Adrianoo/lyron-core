import vosk
import json
import pyaudio

class AudioService:
    def __init__(self, model_path="vosk-model-pt-fb-v0.1.1-20220516_2113"):
        """
        Inicializa o serviço de áudio, carregando o modelo Vosk e abrindo o stream de áudio.
        """
        print("Serviço de Áudio inicializado (Modo Offline com Vosk).")
        try:
            self.model = vosk.Model(model_path)
            self.recognizer = vosk.KaldiRecognizer(self.model, 16000)
            
            self.audio = pyaudio.PyAudio()
            self.stream = self.audio.open(format=pyaudio.paInt16,
                                        channels=1,
                                        rate=16000,
                                        input=True,
                                        frames_per_buffer=8192)
            self.stream.start_stream()
            print("Microfone aberto e pronto.")

        except Exception as e:
            print(f"ERRO: Não foi possível inicializar o serviço de áudio.")
            print(e)
            self.model = None
            self.audio = None
            self.stream = None

    def listen(self):
        """
        Escuta o microfone em um loop contínuo até que um texto válido seja reconhecido.
        Retorna o texto reconhecido ou None se for interrompido.
        """
        if not self.stream:
            print("ERRO: Stream de áudio não está disponível.")
            return None

        print("\nPode falar! Estou ouvindo (offline)...")
        
        while True:
            try:
                data = self.stream.read(4096, exception_on_overflow=False)
                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    text = result.get('text', '')
                    if text:
                        print(f"Texto reconhecido: '{text}'")
                        return text.lower()
            except KeyboardInterrupt:
                print("\nEscuta interrompida pelo usuário.")
                return None
            except Exception as e:
                print(f"Ocorreu um erro inesperado no áudio: {e}")
                return None

    def close(self):
        """
        Fecha o stream de áudio e libera os recursos.
        """
        if self.stream:
            print("Fechando o microfone...")
            self.stream.stop_stream()
            self.stream.close()
        if self.audio:
            self.audio.terminate()
        print("Recursos de áudio liberados.")

if __name__ == '__main__':
    audio_service = AudioService()
    if audio_service.stream:
        texto_ouvido = audio_service.listen()
        if texto_ouvido:
            print(f"\nSUCESSO! O serviço de áudio capturou: '{texto_ouvido}'")
        else:
            print("\nFALHA! O serviço não retornou texto.")
        audio_service.close()
