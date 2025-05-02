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
    dados = pandascore_request("teams", {"search[name]": nome_time, "per_page": 50})

    if not dados:
        return None

    
    times_csgo = [time for time in dados if time.get("current_videogame", {}).get("slug") == "cs-go"]

    return times_csgo  



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

def buscar_stats_jogador(slug):
    dados = pandascore_request("csgo/players", {"search[slug]": slug})
    
    if not dados or len(dados) == 0:
        return None

    return dados[0]  
async def jogador_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jogador_slug = update.message.text.lstrip("/").lower()  
    stats = buscar_stats_jogador(jogador_slug)

    if not stats:
        await update.message.reply_text(
            f"❌ Não encontrei estatísticas para o jogador *{jogador_slug}*.",
            parse_mode="Markdown"
        )
        return

    
    nome = stats.get("name", "Desconhecido")
    first_name = stats.get("first_name", "")
    last_name = stats.get("last_name", "")
    nationality = stats.get("nationality", "N/A")
    
    player_image = stats.get("image_url", None)

    
    texto = (
        f"📋 *Informações de {nome}*\n\n"
        f"*Nome completo:* {first_name} {last_name}\n"
        f"*Nacionalidade:* {nationality}\n"
        
    )

    
    if player_image:
        texto += f"🖼️ [Foto do jogador]({player_image})\n"
    

    await update.message.reply_text(texto, parse_mode="Markdown")

async def lineup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    times = buscar_info_time("furia")
    
    if not times:
        await update.message.reply_text("❌ Não consegui encontrar times da FURIA de CS:GO.")
        return

    texto = "🎯 *Line-up da FURIA:*\n\n"

    for time in times:
        nome_time = time.get("name", "Nome desconhecido")
        jogadores = time.get("players", [])

        texto += f"*{nome_time}:*\n"
        if jogadores:
            for jogador in jogadores:
                nome = jogador.get("name", "Nome desconhecido")
                comando = nome.replace(" ", "_").lower()  # Formata o comando
                texto += f"• /{comando}\n"

                # Adiciona dinamicamente o comando para o jogador
                app.add_handler(CommandHandler(comando, jogador_info))

        else:
            texto += "🕵️‍♂️ Line-up não disponível.\n"
        texto += "\n"

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
