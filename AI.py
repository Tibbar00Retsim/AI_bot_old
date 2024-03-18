from telegram import Bot, Update, InlineKeyboardMarkup, InlineKeyboardButton, ChatAction
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
import g4f
import g4f.image as image # Импортировать модуль g4f.image с другим именем
import logging

# Настройка журналирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Создание экземпляра провайдера
provider = g4f.Provider.Bing

# Создание функции для обработки сообщений
async def handle_message(update: Update, context: CallbackContext) -> None:

    user_message = update.message.text
    # Уведомить пользователя, что бот печатает
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    # Использование g4f с провайдером Bing для генерации ответа
    response = await g4f.ChatCompletion.create_async(model="gpt-4", messages=[{"role": "user", "content": user_message}], provider=provider)
    await update.message.reply_text(response)

# Создание функции для команды /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Привет! Я ваш бот, созданный с использованием g4f и провайдера Bing.')

# Создание функции для команды /image
async def image(update: Update, context: CallbackContext) -> None:
    query = " ".join(context.args) # Получить текстовый запрос для изображения
    if query:
        # Использовать image.ImageCompletion с провайдером Bing и моделью DALL-E 3 для генерации изображения по запросу
        result = await image.ImageCompletion.create_async(model="dalle-3", query=query, provider=provider) # Переименовать переменную image в result
        # Отправить изображение в ответ на команду /image
        await update.message.reply_photo(result) # Использовать переменную result для отправки изображения
    else:
        await update.message.reply_text('Пожалуйста, укажите текстовый запрос для изображения после команды /image')

# Основная функция
def main() -> None:
    # Создание экземпляра ApplicationBuilder и передача токена вашего бота
    application = ApplicationBuilder().token("6910101448:AAFBqzGJM183Jqx4A_wUjn4FoFSAwYYe9sY").build()
    # На разные команды - ответьте в Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("image", image)) # Добавить обработчик для команды /image

    # Обработка текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота
    application.run_polling()

    # Сообщение о статусе бота
    print("Бот запущен и работает...")

if __name__ == '__main__':
    main()
