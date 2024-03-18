from telegram import Bot, Update, InlineKeyboardMarkup, InlineKeyboardButton, ChatAction
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
import g4f
import g4f.image as image
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


provider = g4f.Provider.Bing


async def handle_message(update: Update, context: CallbackContext) -> None:

    user_message = update.message.text
    
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    
    response = await g4f.ChatCompletion.create_async(model="gpt-4", messages=[{"role": "user", "content": user_message}], provider=provider)
    await update.message.reply_text(response)


async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Привет! Я ваш бот, созданный с использованием g4f и провайдера Bing.')


async def image(update: Update, context: CallbackContext) -> None:
    query = " ".join(context.args) 
    if query:
        
        result = await image.ImageCompletion.create_async(model="dalle-3", query=query, provider=provider)
        
        await update.message.reply_photo(result)
    else:
        await update.message.reply_text('Пожалуйста, укажите текстовый запрос для изображения после команды /image')


def main() -> None:
    
    application = ApplicationBuilder().token("token").build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("image", image))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

    print("Бот запущен и работает...")

if __name__ == '__main__':
    main()
