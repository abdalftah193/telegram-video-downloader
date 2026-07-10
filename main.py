from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

TOKEN = "8795590461:AAEJAKzCjyNsSwub17bBeqg40BL7yYTAEHw"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أهلاً 👋\n\nابعتلي أي رابط فيديو وأنا هنزلهولك."
    )

app = Application.builder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, start))

print("Bot Started...")
app.run_polling()
