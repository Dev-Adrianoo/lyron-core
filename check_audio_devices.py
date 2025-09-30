import pyaudio

print("--- Verificando dispositivos de áudio disponíveis para o PyAudio ---")
pa = None
try:
    pa = pyaudio.PyAudio()
    device_count = pa.get_device_count()
    print(f"Encontrados {device_count} dispositivos de áudio no total.")

    found_input = False
    for i in range(device_count):
        device_info = pa.get_device_info_by_index(i)
        if device_info.get('maxInputChannels') > 0:
            print(f"  [ENTRADA] Device {i}: {device_info.get('name')}")
            found_input = True
        else:
            print(f"  [SAÍDA]  Device {i}: {device_info.get('name')}")

    print("-" * 20)
    if found_input:
        print("\n✅ SUCESSO: Pelo menos um dispositivo de entrada (microfone) foi encontrado!")
    else:
        print("\n❌ FALHA: Nenhum dispositivo de entrada (microfone) foi detectado pelo PyAudio no WSL.")

except Exception as e:
    print(f"\n❌ Ocorreu um erro ao inicializar o PyAudio: {e}")
finally:
    if pa:
        pa.terminate()