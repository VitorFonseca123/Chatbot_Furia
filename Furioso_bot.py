from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
from dotenv import load_dotenv
import os
from datetime import datetime





def TELEGRAM_KEY():
    load_dotenv()
    return os.getenv("TELEGRAM_API_KEY")

def ESPORTS_KEY():
    load_dotenv()
    return os.getenv("ESPORTS_API_KEY")

def pandascore_request(endpoint, params=None):
    load_dotenv()
    url = f"https://api.pandascore.co/{endpoint}"
    headers = {"Authorization": f"Bearer {ESPORTS_KEY()}"}
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        print(f"Erro {response.status_code} ao acessar {url}")
        return None
    
    return response.json()

def buscar_info_time(nome_time):
    dados = pandascore_request("teams", {"search[name]": nome_time})
    
    if not dados:
        return None

   
    for time in dados:
        if time.get("current_videogame", {}).get("slug") == "cs-go":
            return time

    return None  


def buscar_proximos_jogos_do_time(nome_time="furia"):
    partidas = pandascore_request("csgo/matches/upcoming", {"per_page": 100})
    if not partidas:
        return None

    for partida in partidas:
        equipes = [team["opponent"]["name"].lower() for team in partida["opponents"] if team.get("opponent")]
        if nome_time.lower() in " ".join(equipes):
            adversario = [
                team["opponent"]["name"] 
                for team in partida["opponents"] 
                if nome_time.lower() not in team["opponent"]["name"].lower()
            ]
            return {
                "adversario": adversario[0] if adversario else "a definir",
                "data": partida["begin_at"][:10],
                "hora": partida["begin_at"][11:16],
                "campeonato": partida["league"]["name"]
            }

    return None





async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    await update.message.reply_text(
        "🔥🐆 *Seja bem-vindo(a) à toca da FURIA!* 🐆🔥\n\n"
        "Aqui é onde a selva se conecta! 🧠💥\n"
        "Fique por dentro das *novidades do time de CS*, receba *notificações de partidas*, participe de *enquetes*, curiosidades, e muito mais!\n\n"
        "Use os comandos abaixo para começar:\n"
        "/proximojogo – Ver próximo jogo\n"
        "/lineup – Ver line-up atual\n"
        "/rank – Ranking e estatísticas\n"
        "/notificacoes – Ativar/desativar alertas de partidas\n\n"
        "_Vamos juntos rugir mais alto. FURIA acima de tudo!_ 🖤🤍",
        parse_mode="Markdown")
    
async def proximo_jogo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jogo = buscar_proximos_jogos_do_time()
    if jogo:
        msg = (
            f"🎮 *Próximo jogo da FURIA!*\n\n"
            f"🗓️ Data: *{jogo['data']}*\n"
            f"⏰ Horário: *{jogo['hora']}*\n"
            f"🆚 Adversário: *{jogo['adversario']}*\n"
            f"🏆 Campeonato: *{jogo['campeonato']}*\n\n"
            f"🐆 Vamos pra cima, FURIOSO!"
        )
    else:
        msg = "😕 Não encontrei partidas futuras da FURIA no momento."

    await update.message.reply_text(msg, parse_mode="Markdown")

async def lineup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    time = buscar_info_time("furia")
    
    if not time:
        await update.message.reply_text("❌ Não consegui encontrar o time de csgo da FURIA.")
        return

    jogadores = time.get("players", [])

    if not jogadores:
        await update.message.reply_text("🕵️‍♂️ A line-up atual da FURIA não está disponível na API.")
        return

    texto = "🎯 *Line-up atual da FURIA:*\n\n"
    for jogador in jogadores:
        nome = jogador.get("name", "Nome desconhecido")
        nick = jogador.get("slug", "")
        texto += f"• `{nick}` – {nome}\n"

    await update.message.reply_text(texto, parse_mode="Markdown")

app = ApplicationBuilder().token(TELEGRAM_KEY()).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("proximojogo", proximo_jogo))
app.add_handler(CommandHandler("lineup", lineup))


'''def listar_times_futuros():
    url = "https://api.pandascore.co/csgo/matches/upcoming?page=1&per_page=100"
    headers = {"Authorization": f"Bearer {ESPORTS_KEY()}"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Erro ao acessar a API:", response.status_code)
        return

    partidas = response.json()
    times = set()

    for partida in partidas:
        for opponent in partida.get("opponents", []):
            team = opponent.get("opponent", {})
            nome = team.get("name")
            if nome:
                times.add(nome)

    print("✅ Times encontrados nos próximos jogos:")
    for nome in sorted(times):
        print("-", nome)

listar_times_futuros()'''
app.run_polling()
