
import subprocess
import os
import platform
import wave
import simpleaudio as sa

def is_running_in_wsl():
    """Verifica se o script está rodando dentro do WSL."""
    return 'microsoft' in platform.uname().release.lower() or 'wsl' in platform.uname().release.lower()

class TTSService:
    def __init__(self, model_name='pt_BR-faber-medium.onnx'):
        print("Serviço de TTS (Voz) Inicializado.")

        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.piper_path = os.path.join(script_dir, 'tts', 'piper', 'piper')
        self.model_path = os.path.join(script_dir, 'tts', 'voices', model_name)
        self.output_path = os.path.join(script_dir, 'tts', 'output.wav')

        if not os.path.exists(self.piper_path):
            print(f"--- ALERTA TTS ---")
            print(f"Executável do Piper não encontrado em: {self.piper_path}")
            print("Por favor, baixe o Piper e coloque-o na pasta tts/piper/")
            print("Download: https://github.com/rhasspy/piper/releases")
            print("--------------------")

    def speak(self, text):
        if not text:
            print("TTS: Nenhum texto para falar.")
            return

        print(f"TTS: Gerando áudio para o texto -> {text}")

        command = [
            self.piper_path,
            '--model', self.model_path,
            '--output_file', self.output_path
        ]

        try:
            subprocess.run(command, input=text, encoding='utf-8', check=True,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            print("TTS: Reprodzindo áudio...")

            if is_running_in_wsl():
                self._play_audio_in_wsl()
            else:
                self._play_audio_default()

        except FileNotFoundError:
            print(f"ERROR TTS: O executável do Piper não foi encontrando em '{self.piper_path}'")
        except subprocess.CalledProcessError as e:
            print(f"ERRO TTS: O piper falhou ao gerar áudio: {e}")
        except Exception as e:
            print(f"ERRO TTS: Ocorreu um erro inesperado ao tocar o áudio: {e}")
        finally:
            if os.path.exists(self.output_path):
                os.remove(self.output_path)

    def _play_audio_default(self):
        """Método padrão para tocar áudio, usado em Linux nativo (Raspberry Pi)."""
        wave_obj = sa.WaveObject.from_wave_file(self.output_path)
        play_obj = wave_obj.play()
        play_obj.wait_done()

    def _play_audio_in_wsl(self):
        """Método de contorno para tocar áudio no WSL, usando PowerShell."""
        try:
            result = subprocess.run(['wslpath', '-w', self.output_path], capture_output=True, text=True, check=True)
            windows_path = result.stdout.strip()

            ps_command = f"(New-Object Media.SoundPlayer '{windows_path}').PlaySync();"
            
            subprocess.run(['powershell.exe', '-Command', ps_command], check=True)
        except FileNotFoundError:
            print("ERRO TTS (WSL): 'wslpath' ou 'powershell.exe' não encontrado. Verifique sua instalação do WSL.")
        except Exception as e:
            print(f"ERRO TTS (WSL): Falha ao tentar tocar áudio via PowerShell: {e}")

