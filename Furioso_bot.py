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

def buscar_proximos_jogos_do_time(nome_time="pain"):
    url = "https://api.pandascore.co/lol/matches/upcoming"
    headers = {"Authorization": f"Bearer {ESPORTS_KEY()}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print("Erro ao acessar API:", response.status_code)
        return None

    partidas = response.json()

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
    await update.message.reply_text("🔥🐆 *Seja bem-vindo(a) à toca da FURIA!* 🐆🔥\n\n"
        "Aqui é onde a selva se conecta! 🧠💥\n"
        "Fique por dentro das *novidades do time de CS*, receba *notificações de partidas*, participe de *enquetes*, curiosidades, e muito mais!\n\n"
        "Use os comandos abaixo para começar:\n"
        "/proximojogo – Ver próximo jogo\n"
        "/jogos – Ver próximos jogos\n"
        "/rank – Ranking e estatísticas\n"
        "/curiosidades – Fatos interessantes da FURIA\n"
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
    

app = ApplicationBuilder().token(TELEGRAM_KEY()).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("proximojogo", proximo_jogo))


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
