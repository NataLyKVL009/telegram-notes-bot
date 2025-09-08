from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
TOKEN = os.getenv("BOT_TOKEN")

# Вставь сюда токен от BotFather
#TOKEN = "8449212884:AAEp-8TFw_tYj8xXL1ecVLrqlyWdSODeIF4"

# ⚡️ вставь сюда свой admin_id (узнаешь через /myid)
ADMIN_ID = 123456789

# ⚡️ вставь сюда свой токен
TOKEN = "YOUR_BOT_TOKEN"

feedbacks = []

# Главное меню
main_menu = ReplyKeyboardMarkup(
    [
        ["✍️ Добавить отзыв", "ℹ️ Помощь"],
        ["📋 Все отзывы (только админ)"]
    ],
    resize_keyboard=True
)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! 👋\nВыбери действие из меню ниже:",
        reply_markup=main_menu
    )

# Добавление отзыва
async def add_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # проверяем, нажата ли кнопка
    if update.message.text == "✍️ Добавить отзыв":
        await update.message.reply_text("Напиши свой отзыв одним сообщением:")
        return

    # если пользователь написал текст → сохраняем его как отзыв
    feedbacks.append((update.message.from_user.username, update.message.text))
    await update.message.reply_text("Спасибо! Твой отзыв сохранён ✅")

# Показ всех отзывов
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

# Помощь
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Доступные действия:\n\n"
        "✍️ Добавить отзыв – оставить свой отзыв\n"
        "📋 Все отзывы – доступно только администратору\n"
        "ℹ️ Помощь – показать это сообщение"
    )

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, add_feedback))
    app.add_handler(MessageHandler(filters.Regex("📋 Все отзывы"), all_feedbacks))
    app.add_handler(MessageHandler(filters.Regex("ℹ️ Помощь"), help_command))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()