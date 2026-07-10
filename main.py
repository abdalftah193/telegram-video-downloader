from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = "8795590461:AAEJAKzCjyNsSwub17bBeqg40BL7yYTAEHw"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أهلاً 👋\n\nابعتلي لينك فيديو من YouTube أو TikTok أو Instagram أو Facebook."
    )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    print("Bot Started...")
    app.run_polling()


if __name__ == "__main__":
    main()
