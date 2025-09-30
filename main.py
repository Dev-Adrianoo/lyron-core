from audio_service import AudioService
from ai_service import AIService
from tts_service import TTSService
from arduino_service import ArduinoService 
from fake_arduino_service import FakeArduinoService
import os
import struct
import pyaudio
import pvporcupine

USE_REAL_ARDUINO = False
ARDUINO_PORT = '/dev/ttyACM0'
COMANDOS_CONHECIDOS = ["ACENAR", "FELIZ", "CONFUSO", "DORMINDO"]

PICOVOICE_ACCESS_KEY = os.getenv("PICOVOICE_ACCESS_KEY")
keyword_path = './wakewords/Iniciar-escuta_pt_linux_v3_0_0.ppn'

def listen_for_wakeword(porcupine, audio_stream):
    """
    Ouve passivamente pelo microfone e retorna True se a palavra de ativação for detectada.
    """
    try:
        pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
        keyword_index = porcupine.process(pcm)
        if keyword_index >= 0:
            return True
    except (IOError, struct.error) as e:
        print(f"Erro no Porteiro (Wake Word): {e}")
    return False

def main():
    
    porcupine = None
    pa = None
    porcupine_audio_stream = None
    arduino = None
    audio = None 

    try: 
        print("--- Lyron: Iniciando sistemas ---")

        
        audio = AudioService() 
        ia = AIService()
        tts = TTSService()

        if USE_REAL_ARDUINO:
            arduino = ArduinoService(port=ARDUINO_PORT)
        else:
            arduino = FakeArduinoService(port="porta_falsa")
      
        if not arduino.connect():
            print("ERRO CRÍTICO: Não foi possível conectar ao corpo do robô. Encerrando.")
            return
        
        model_path = './models/porcupine_params_pt.pv'

        porcupine = pvporcupine.create(
            access_key=PICOVOICE_ACCESS_KEY,
            keyword_paths=[keyword_path],
            model_path=model_path 
        )
        
        pa = pyaudio.PyAudio()
        porcupine_audio_stream = pa.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )

        tts.speak("Sistema online. Estou pronto para conversar.")
        arduino.send_command("FELIZ")

        print("\n--- Lyron está aguardando a palavra de ativação ---")

        
        while True:
           
            if listen_for_wakeword(porcupine, porcupine_audio_stream):
                print("\nPalavra de ativação detectada!")
                arduino.send_command("CONFUSO") 
                tts.speak("Pois não? estou aqui")

                
                texto_usuario = audio.listen()

                if texto_usuario:
                    
                    resposta_ia = ia.get_ai_response(texto_usuario)
                    print(f'Lyron pensou: "{resposta_ia}"')

                    
                    tts.speak(resposta_ia)
                    
                    
                    comando_encontrado = False
                    for comando in COMANDOS_CONHECIDOS:
                        if comando.lower() in resposta_ia.lower():
                            print(f"Comando encontrado na resposta: {comando}")
                            arduino.send_command(comando)
                            comando_encontrado = True
                            break 
                    
                    if not comando_encontrado:
                        arduino.send_command("FELIZ") 
                
                print("\n--- Lyron está aguardando a palavra de ativação ---")

    except KeyboardInterrupt:
        print("\nDetectado Ctrl+C. Encerrando de forma limpa.")

    finally:
        
        print("--- Encerrando sistemas. Até mais! ---")
        try:
            if porcupine:
                porcupine.delete()
            if porcupine_audio_stream:
                porcupine_audio_stream.close()
            if pa:
                pa.terminate()
            if audio:
                audio.close()
            if arduino:
                tts.speak("Desligando.")
                arduino.disconnect()
        except Exception as e:
            print(f"Ocorreu um erro durante o encerramento: {e}")

if __name__ == "__main__":
    main()
