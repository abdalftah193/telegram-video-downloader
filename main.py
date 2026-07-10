from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

TOKEN = "حط التوكن الجديد هنا"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أهلاً 👋\n\nابعتلي أي رابط فيديو وأنا هنزلهولك."
    )

app = Application.builder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, start))

print("Bot Started...")
app.run_polling()
