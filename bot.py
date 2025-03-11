import os
from flask import Flask
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import threading

app_flask = Flask(__name__)

# HTTP-эндпоинт для пингов (чтобы избежать засыпания)
@app_flask.route('/')
def keep_alive():
    return "Bot is alive!", 200

# Инициализация бота
TOKEN = os.getenv("TOKEN")
MODEL_NAME = "distilgpt2"  # Лёгкая модель для Heroku (512 MB RAM)

# Заглушка для генерации ответа (без модели для теста)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Добро пожаловать! Я Grok 3 Premium от xAI. Чем могу помочь?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    response = f"Я получил: {user_message} (заглушка, модель пока не подключена)"
    await update.message.reply_text(response)

# Настройка бота
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Запуск Flask в отдельном потоке
def run_flask():
    port = int(os.getenv("PORT", 5000))
    app_flask.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    print("Bot is running...")
    # Запускаем Flask в отдельном потоке
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    # Запускаем Telegram-бота
    app.run_polling()