import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

TOKEN = "8795590461:AAEMDeKwBHFeioAI0sM_PdVvJDhchypxHaY"

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    msg = await update.message.reply_text("⏳ جاري تحميل الفيديو...")

    try:
        ydl_opts = {
            "cookiefile": os.path.abspath("cookies.txt"),
            "outtmpl": os.path.join(DOWNLOAD_DIR, "video.%(ext)s"),
            "format": "best",
            "noplaylist": True,
        }

        print("Starting download...")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        print("Download finished")
print(filename)
print(os.path.getsize(filename))

await msg.edit_text("📤 جاري إرسال الفيديو...")
print("Starting upload...")

        with open(filename, "rb") as video:
            await update.message.reply_video(
    video=video,
    read_timeout=600,
    write_timeout=600,
    connect_timeout=60,
)

print("Upload finished")

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
