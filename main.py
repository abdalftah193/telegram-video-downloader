import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

TOKEN = "8795590461:AAExwG4Sukmf2QT39RmRS7iNNpKYPWTm4vg"

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    msg = await update.message.reply_text("⏳ جاري تحميل الفيديو...")

    try:
        ydl_opts = {
            "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
            "format": "best"
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        await msg.edit_text("📤 جاري إرسال الفيديو...")

        with open(filename, "rb") as video:
            await update.message.reply_video(video=video)

        os.remove(filename)

        await msg.delete()

    except Exception as e:
        await msg.edit_text(f"❌ حدث خطأ:\n{e}")


app = Application.builder().token(TOKEN).build()

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, download)
)

print("Bot Started...")

app.run_polling()
