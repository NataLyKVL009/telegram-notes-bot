from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
TOKEN = os.getenv("BOT_TOKEN")

# Вставь сюда токен от BotFather
#TOKEN = "8449212884:AAEp-8TFw_tYj8xXL1ecVLrqlyWdSODeIF4"

# Простое хранилище заметок (в памяти)
notes = {}


# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот для заметок 📝\n"
                                    "Просто напиши мне заметку.\n"
                                    "Команды:\n"
                                    "/notes – показать все заметки\n"
                                    "/clear – удалить все заметки")


# Добавление заметки
async def add_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    if user_id not in notes:
        notes[user_id] = []
    notes[user_id].append(text)

    await update.message.reply_text(f"✅ Заметка сохранена: {text}")


# Показать все заметки
async def show_notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_notes = notes.get(user_id, [])

    if not user_notes:
        await update.message.reply_text("У тебя пока нет заметок.")
    else:
        result = "\n".join([f"{i + 1}. {n}" for i, n in enumerate(user_notes)])
        await update.message.reply_text(f"📒 Твои заметки:\n{result}")


# Очистить все заметки
async def clear_notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    notes[user_id] = []
    await update.message.reply_text("🗑 Все заметки удалены.")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("notes", show_notes))
    app.add_handler(CommandHandler("clear", clear_notes))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, add_note))

    app.run_polling()


if __name__ == "__main__":
    main()
