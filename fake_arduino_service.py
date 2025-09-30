class FakeArduinoService:
  """
  Um "dublê" do nosso ArduinoService. Não se conecta a hardware real,
  apenas imprime na tela o que faria. Perfeito para testes.
  """

  def __init__(self, port, bound_rate=9600):
    print(f"--- [Fake Arduino] Serviço inicializado para porta '{port}'. ---")
  
  def connect(self):
    print("[Fake Arduino] Conexão simulada com sucesso.")
    return True


  def send_command(self, command):
    print(f"[ Fake Arduino ] Comando enviado {command}")

  def disconnect(self):
    print("[Fake Arduino] Conexão simulada encerrada.")