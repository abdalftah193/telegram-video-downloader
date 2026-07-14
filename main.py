import os
import glob
import subprocess
from telegram import Update, InputFile
from telegram.ext import Application, MessageHandler, ContextTypes, filters

TOKEN = "8795590461:AAEqvG15FvyEPiFpEbrS22zyBisI90EkXrQ"

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    msg = await update.message.reply_text("⏳ جاري تحميل الفيديو...")

    try:
        print("Starting download...")

        subprocess.run([
            "yt-dlp",
            "--cookies", os.path.abspath("cookies.txt"),
            "-f", "best",
            "-o", os.path.join(DOWNLOAD_DIR, "video.%(ext)s"),
            url
        ], check=True)

        files = glob.glob(os.path.join(DOWNLOAD_DIR, "video.*"))
        if not files:
            raise Exception("Download failed")

        filename = files[0]

        print("Download finished")
        print(filename)

        await msg.edit_text("📤 جاري إرسال الفيديو...")

        with open(filename, "rb") as video:
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=InputFile(video),
                filename=os.path.basename(filename),
                read_timeout=600,
                write_timeout=600,
                connect_timeout=60,
                pool_timeout=60,
            )

        os.remove(filename)
        await msg.delete()

    except Exception as e:
        print(e)
        await msg.edit_text(f"❌ حدث خطأ:\n{e}")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, download)
    )

    print("Bot Started...")
    app.run_polling()


if __name__ == "__main__":
    main()
