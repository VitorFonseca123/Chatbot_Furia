from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from dotenv import load_dotenv
import os




def API_KEY():
    load_dotenv()
    api_key = os.getenv("API_KEY")
    return api_key


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
    

app = ApplicationBuilder().token(API_KEY()).build()
app.add_handler(CommandHandler("start", start))

app.run_polling()
