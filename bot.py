import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from shazamio import Shazam

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎵 ARTIST UZ ga xush kelibsiz!\n\n"
        "Musiqa, ovozli xabar yoki video yuboring — qo‘shiqni topaman."
    )

async def music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    media = msg.audio or msg.voice or msg.video or msg.document

    if not media:
        return

    file = await context.bot.get_file(media.file_id)
    path = "music_file"
    await file.download_to_drive(path)

    try:
        shazam = Shazam()
        result = await shazam.recognize(path)
        track = result.get("track")

        if track:
            await msg.reply_text(
                f"🎵 Qo‘shiq: {track.get('title')}\n"
                f"🎤 Ijrochi: {track.get('subtitle')}"
            )
        else:
            await msg.reply_text("😔 Qo‘shiq topilmadi.")
    except Exception:
        await msg.reply_text("Xatolik yuz berdi. Qayta urinib ko‘ring.")
    finally:
        if os.path.exists(path):
            os.remove(path)

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.AUDIO | filters.VOICE | filters.VIDEO | filters.Document.ALL, music))
app.run_polling()
