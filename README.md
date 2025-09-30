# Lyron Core - Assistente de Voz Robótico

Lyron Core é o cérebro de um assistente de voz robótico de mesa. Ele foi projetado para rodar localmente, utilizando tecnologias de código aberto para detecção de palavra de ativação, reconhecimento de fala, processamento de linguagem natural e síntese de voz.

## Funcionalidades

- **Detecção de Palavra de Ativação (Wake Word):** Escuta passivamente pelo comando "Iniciar Escuta" usando o `Porcupine`.
- **Reconhecimento de Fala Offline:** Transcreve a fala do usuário para texto usando o `Vosk`.
- **Inteligência Artificial Local:** Gera respostas utilizando um modelo de linguagem grande (LLM) através do `Ollama`.
- **Personalidade Única:** Lyron é configurado para ser um robô de mesa cômico, sarcástico e curioso.
- **Síntese de Voz (TTS) Offline:** Converte o texto da resposta em áudio usando o `Piper`.
- **Controle de Hardware:** Envia comandos para um microcontrolador (Arduino) para controlar um corpo robótico.

---

## 1. Pré-requisitos

Antes de começar, você precisará ter os seguintes softwares instalados:

- **Python 3.8+**
- **Git**
- **Ollama:** Siga as instruções de instalação em [ollama.com](https://ollama.com/).
- **PortAudio:** Necessário para a biblioteca `PyAudio`.
  - No Debian/Ubuntu: `sudo apt-get install portaudio19-dev`
  - No Fedora: `sudo dnf install portaudio-devel`
  - No macOS (usando Homebrew): `brew install portaudio`

## 2. Instalação

Siga os passos abaixo para configurar o ambiente do Lyron.

### a. Clone o Repositório

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd lyron-core
```

### b. Crie um Ambiente Virtual e Instale as Dependências

É altamente recomendado usar um ambiente virtual para isolar as dependências do projeto.

```bash
# Crie o ambiente virtual
python -m venv venv

# Ative o ambiente
source venv/bin/activate

# Instale as bibliotecas Python
pip install -r requirements.txt
```

### c. Faça o Download dos Modelos

O Lyron depende de modelos de machine learning que **não estão** no repositório. Você precisa baixá-los e colocá-los nas pastas corretas.

#### i. Modelo de Reconhecimento de Fala (Vosk)

- **Modelo:** `vosk-model-small-pt-0.3`
- **Download:** [Clique aqui para baixar](https://alphacephei.com/vosk/models/vosk-model-small-pt-0.3.zip)
- **Instruções:**
  1. Descompacte o arquivo.
  2. Renomeie a pasta para `vosk-model-small-pt-0.3`.
  3. Mova a pasta para a raiz do projeto `lyron-core/`.

#### ii. Modelo de Síntese de Voz (Piper)

- **Executor do Piper:**
  - **Download:** Vá para a [página de releases do Piper](https://github.com/rhasspy/piper/releases) e baixe a versão `piper_linux_x86_64.tar.gz` (ou a apropriada para seu sistema).
  - **Instruções:**
    1. Descompacte o arquivo.
    2. Mova o conteúdo (a pasta `piper` e seus arquivos) para dentro da pasta `tts/` do projeto. A estrutura final deve ser `lyron-core/tts/piper/piper`.

- **Voz (pt_BR-faber-medium):**
  - **Download:** [Clique aqui para baixar o modelo de voz](https://huggingface.co/rhasspy/piper-voices/resolve/main/pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx?download=true) e [o arquivo de configuração](https://huggingface.co/rhasspy/piper-voices/resolve/main/pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx.json?download=true).
  - **Instruções:**
    1. Crie a pasta `lyron-core/tts/voices/`.
    2. Coloque os dois arquivos (`.onnx` e `.onnx.json`) dentro desta pasta.

#### iii. Modelos de Palavra de Ativação (Porcupine)

- **Palavra de Ativação "Iniciar Escuta":**
  - **Download:** *[Insira aqui o link para download do seu arquivo `Iniciar-escuta_pt_linux_v3_0_0.zip` ou similar]*
  - **Instruções:**
    1. Crie a pasta `lyron-core/wakewords/`.
    2. Descompacte o arquivo e coloque o arquivo `.ppn` dentro desta pasta.

- **Parâmetros do Modelo (Português):**
  - **Download:** *[Insira aqui o link para download do seu arquivo `porcupine_params_pt.pv`]*
  - **Instruções:**
    1. Crie a pasta `lyron-core/models/`.
    2. Coloque o arquivo `.pv` dentro desta pasta.

### d. Configure o Modelo de IA (Ollama)

Após instalar o Ollama, puxe o modelo que o Lyron usa:

```bash
ollama pull phi3:mini
```

Certifique-se de que o serviço do Ollama esteja rodando em segundo plano antes de iniciar o Lyron.

---

## 3. Configuração

### Chave de Acesso do Picovoice

O Porcupine requer uma chave de acesso.

1. Crie uma conta gratuita no [Picovoice Console](https://console.picovoice.ai/).
2. Copie sua `Access Key`.
3. Crie um arquivo chamado `.env` na raiz do projeto e adicione sua chave a ele:

   ```
   PICOVOICE_ACCESS_KEY="SUA_CHAVE_DE_ACESSO_AQUI"
   ```

### Configuração do Arduino

No arquivo `main.py`, você pode alternar entre um Arduino real e um simulado:

- `USE_REAL_ARDUINO = True`: Para usar um Arduino físico.
  - Altere `ARDUINO_PORT` para a porta serial correta (ex: `/dev/ttyACM0` no Linux).
- `USE_REAL_ARDUINO = False`: Para usar um serviço falso que apenas imprime os comandos no console (útil para testes sem hardware).

O código para o corpo do robô está em `wokwi-body/wokwi.ino` e pode ser usado com o simulador [Wokwi](https://wokwi.com/) ou gravado em um Arduino real.

---

## 4. Executando o Projeto

Com tudo configurado, ative seu ambiente virtual e inicie o programa:

```bash
# Ative o ambiente (se não estiver ativo)
source venv/bin/activate

# Execute o script principal
python main.py
```

O terminal mostrará o status de inicialização dos sistemas. Quando a mensagem "Lyron está aguardando a palavra de ativação" aparecer, diga "Iniciar Escuta" e comece a interagir!
