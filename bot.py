import os
import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
AUDD_TOKEN = os.getenv("AUDD_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎵 ARTIST UZ botiga xush kelibsiz!\n\n"
        "Musiqa yoki video yuboring. Qo‘shiq nomini topib beraman."
    )

async def music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    file = await msg.effective_attachment.get_file()
    path = "music_file"
    await file.download_to_drive(path)

    try:
        with open(path, "rb") as audio:
            response = requests.post(
                "https://api.audd.io/",
                data={"api_token": AUDD_TOKEN, "return": "spotify,apple_music"},
                files={"file": audio},
                timeout=60
            ).json()

        result = response.get("result")

        if result:
            text = (
                f"🎵 Qo‘shiq: {result.get('title')}\n"
                f"🎤 Ijrochi: {result.get('artist')}\n"
                f"💿 Albom: {result.get('album') or 'Noma’lum'}"
            )
            await msg.reply_text(text)
        else:
            await msg.reply_text("😔 Musiqa topilmadi. Boshqa parcha yuboring.")

    except Exception:
        await msg.reply_text("Xatolik yuz berdi. Qayta urinib ko‘ring.")
    finally:
        if os.path.exists(path):
            os.remove(path)

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.AUDIO | filters.VOICE | filters.VIDEO | filters.Document.AUDIO, music))
app.run_polling()
