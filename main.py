from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
TOKEN = os.getenv("BOT_TOKEN")

# Вставь сюда токен от BotFather
#TOKEN = "8449212884:AAEp-8TFw_tYj8xXL1ecVLrqlyWdSODeIF4"

# ⚡️ вставь сюда свой admin_id (узнаешь через /myid)
ADMIN_ID = 123456789

# Храним отзывы в памяти (можно потом заменить на БД или файл)
feedbacks = []

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Отправь отзыв с помощью команды:\n"
        "/add твой_текст"
    )

# Команда /add <отзыв>
async def add_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Напиши отзыв после команды. Пример:\n/add Отличный сервис!")
        return

    feedback = " ".join(context.args)
    feedbacks.append((update.message.from_user.username, feedback))

    await update.message.reply_text("Спасибо! Твой отзыв сохранён ✅")

# Команда /all (доступна только админу)
async def all_feedbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("⛔ У тебя нет прав для просмотра отзывов.")
        return

    if not feedbacks:
        await update.message.reply_text("Пока нет отзывов.")
        return

    text = "📋 Список отзывов:\n\n"
    for username, fb in feedbacks:
        text += f"👤 @{username if username else 'Без ника'}:\n{fb}\n\n"

    await update.message.reply_text(text)

# Команда /myid (чтобы узнать свой id)
async def my_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    await update.message.reply_text(f"Твой Telegram ID: {user_id}")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add_feedback))
    app.add_handler(CommandHandler("all", all_feedbacks))
    app.add_handler(CommandHandler("myid", my_id))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()