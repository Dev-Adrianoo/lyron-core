import serial
import time

class ArduinoService:
  def __init__(self, port, baud_rate=9600):
    self.port = port
    self.baud_rate = baud_rate
    self.connection = None
    print(f"Serviço Arduino inicializado para a porta {self.port}.")

    def connect(self):
      try:
        self.connection = serial.Serial(self.port, self.baud_rate, timeout=2)
        time.sleep(2)
        print("Conexão estabelecida com Sucesso!")
        return True
      except serial.SerialException as e:
        print(f"Erro ao conectar com arduino {e}")
        return False 
      
    def send_command(self, command):
      if self.connection and self.connection.is_open:
        print(f"Enviando comando: {command}")
        self.connection.write(f"{command}\n".encode('utf-8'))
      else:
        print("Não foi possivel enviar comando. Conexão não está ativa.")
    
    def disconnect(self):
      if self.connection and self.connection.is_open:
        self.connection.close()
        print("Conexão com arduino encerrada.")