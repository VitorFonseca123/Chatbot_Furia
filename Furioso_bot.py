from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from dotenv import load_dotenv
import os
from datetime import datetime





def API_KEY():
    load_dotenv()
    api_key = os.getenv("API_KEY")
    return api_key

proximos_jogos = [
    {"data": "2025-04-25", "hora": "18:00", "adversario": "NAVI", "campeonato": "ESL Pro League"},
    {"data": "2025-04-27", "hora": "16:00", "adversario": "Vitality", "campeonato": "Blast Premier"},
]




async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔥🐆 *Seja bem-vindo(a) à toca da FURIA!* 🐆🔥\n\n"
        "Aqui é onde a selva se conecta! 🧠💥\n"
        "Fique por dentro das *novidades do time de CS*, receba *notificações de partidas*, participe de *enquetes*, curiosidades, e muito mais!\n\n"
        "Use os comandos abaixo para começar:\n"
        "/jogos – Ver próximos jogos\n"
        "/rank – Ranking e estatísticas\n"
        "/curiosidades – Fatos interessantes da FURIA\n"
        "/notificacoes – Ativar/desativar alertas de partidas\n\n"
        "_Vamos juntos rugir mais alto. FURIA acima de tudo!_ 🖤🤍",
        parse_mode="Markdown")
    
async def proximo_jogo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    hoje = datetime.now().date()

    for jogo in proximos_jogos:
        data_jogo = datetime.strptime(jogo["data"], "%Y-%m-%d").date()
        if data_jogo >= hoje:
            resposta = (
                f"🎮 *Próximo jogo da FURIA!*\n\n"
                f"🗓️ Data: *{jogo['data']}*\n"
                f"⏰ Horário: *{jogo['hora']}*\n"
                f"🆚 Adversário: *{jogo['adversario']}*\n"
                f"🏆 Campeonato: *{jogo['campeonato']}*\n\n"
                f"🐆 Vamos pra cima, FURIOSO!"
            )
            await update.message.reply_text(resposta, parse_mode="Markdown")
            return

    await update.message.reply_text("🐆 Não há jogos programados para os próximos dias. Fique ligado!")
    

app = ApplicationBuilder().token(API_KEY()).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("proximojogo", proximo_jogo))

app.run_polling()
