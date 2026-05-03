import discord
import os
import requests
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém as configurações das variáveis de ambiente
DISCORD_BOT_KEY = os.getenv('DISCORD_BOT_KEY')
AI_API_URL = os.getenv('AI_API_URL')
AI_API_KEY = os.getenv('AI_API_KEY')
AI_SYSTEM_PROMPT = os.getenv('AI_PROMPT')
AI_MODEL = os.getenv('AI_MODEL', 'gemini-1.5-flash-latest')

# Configura as intenções (intents) do bot.
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# Cria a instância do cliente do bot
class BotClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

client = BotClient(intents=intents)

@client.event
async def on_ready():
    """Evento disparado quando o bot está online e pronto."""
    print(f'Bot logado como {client.user}')
    print('------')

def get_ai_response(user_input: str) -> str:
    """
    Função MODIFICADA para se conectar à API do Google Gemini e obter uma resposta.
    """
    if not all([AI_API_URL, AI_API_KEY, AI_SYSTEM_PROMPT]):
        return "Erro: As variáveis de ambiente da IA não foram configuradas corretamente."

    # 1. A chave da API do Google é enviada como um parâmetro na URL.
    url_with_key = f"{AI_API_URL}?key={AI_API_KEY}"
    
    headers = {
        'Content-Type': 'application/json'
    }

    # 2. O payload é adaptado para o formato "contents" do Gemini.
    #    O prompt do sistema é enviado como a primeira mensagem do usuário,
    #    seguido por uma resposta curta do modelo para estabelecer o contexto.
    payload = {
        'contents': [
            {'role': 'user', 'parts': [{'text': AI_SYSTEM_PROMPT}]},
            {'role': 'model', 'parts': [{'text': "Entendido. Estou pronto para agir conforme a persona solicitada."}]},
            {'role': 'user', 'parts': [{'text': user_input}]}
        ]
    }

    response = None  # Inicializa a variável response
    try:
        response = requests.post(url_with_key, headers=headers, json=payload, timeout=120)
        
        # Lança um erro para códigos de status HTTP 4xx/5xx, facilitando o debug.
        response.raise_for_status()

        data = response.json()
        
        # 3. O caminho para extrair o texto da resposta é específico do Gemini.
        #    Adicionamos verificações para garantir que a resposta tenha o formato esperado.
        if 'candidates' in data and data['candidates'] and 'content' in data['candidates'][0] and 'parts' in data['candidates'][0]['content'] and data['candidates'][0]['content']['parts']:
            return data['candidates'][0]['content']['parts'][0]['text'].strip()
        else:
            return f"Não encontrei o conteúdo esperado na resposta da IA. Resposta recebida: {response.text}"
            
    except requests.exceptions.HTTPError as e:
        # Erro específico para respostas HTTP ruins (ex: chave de API inválida, erro 400).
        return f"Lamento, mas encontrei um erro ao consultar a sabedoria. (Código: {e.response.status_code} - {e.response.text})"
    except requests.exceptions.RequestException as e:
        return f"Houve uma falha na comunicação. Por favor, tente novamente mais tarde. (Erro: {e})"
    except (KeyError, IndexError) as e:
        # Caso a estrutura do JSON mude ou venha vazia.
        resposta_texto = response.text if response is not None else "Nenhuma resposta recebida."
        return f"Não consegui interpretar a resposta recebida. (Erro de formato: {e} - Resposta: {resposta_texto})"

@client.tree.command(name="jesus", description="Envie uma mensagem para receber a sabedoria de Jesus.")
async def bot(interaction: discord.Interaction, *, mensagem: str):
    """
    Comando slash para interagir com o bot.
    """
    await interaction.response.defer(thinking=True)
    
    print(f"Mensagem recebida de {interaction.user}: {mensagem}")
    
    response_text = get_ai_response(mensagem)
    
    await interaction.followup.send(f"> {mensagem}\n\n{response_text}")


# Inicia o bot com o token
if DISCORD_BOT_KEY:
    client.run(DISCORD_BOT_KEY)
else:
    print("Error: DISCORD_BOT_KEY variable missing. Verify your .env file")