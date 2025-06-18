import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from openai import OpenAI

# Конфигурация
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# Обработчик команды /start
async def start(update: Update, context):
    await update.message.reply_text("Привет! Я ChatGPT-бот. Задай мне вопрос.")

# Обработчик текстовых сообщений
async def chatgpt_reply(update: Update, context):
    user_message = update.message.text
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_message}],
        temperature=0.7,
    )
    await update.message.reply_text(response.choices[0].message.content)

# Запуск бота
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Регистрация обработчиков
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chatgpt_reply))
    
    # Режим вебхука (для Railway)
    app.run_webhook(
        listen="0.0.0.0",
        port=8000,
        webhook_url="https://your-project.up.railway.app",
    )

if __name__ == "__main__":
    main()
