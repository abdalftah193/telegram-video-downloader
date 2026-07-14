import os
import glob
import subprocess
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

TOKEN = "8795590461:AAEqvG15FvyEPiFpEbrS22zyBisI90EkXrQ"

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    msg = await update.message.reply_text("⏳ جاري التحميل...")

    try:
        # حذف أي ملف قديم
        for f in glob.glob(os.path.join(DOWNLOAD_DIR, "video.*")):
            os.remove(f)

        cmd = [
            "yt-dlp",
            "--cookies", "cookies.txt",
            "--merge-output-format", "mp4",
            "--no-progress",
            "-o", os.path.join(DOWNLOAD_DIR, "video.%(ext)s"),
            url,
        ]

        subprocess.run(cmd, check=True)

        files = glob.glob(os.path.join(DOWNLOAD_DIR, "video.*"))
        if not files:
            raise Exception("لم يتم العثور على الفيديو")

        filename = files[0]

        await msg.edit_text("📤 جاري الإرسال...")

        with open(filename, "rb") as f:
            await update.message.reply_document(document=f)

        os.remove(filename)
        await msg.delete()

    except Exception as e:
        print(e)
        await msg.edit_text(f"❌ {e}")


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))

    print("Bot Started...")
    app.run_polling()


if __name__ == "__main__":
    main()
