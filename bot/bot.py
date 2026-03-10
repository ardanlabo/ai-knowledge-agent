import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

from database.db import init_db, insert_item

# Load environment variables
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ALLOWED_USER_ID = os.getenv("TELEGRAM_ALLOWED_USER_ID")

if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN missing in .env")

if not ALLOWED_USER_ID:
    raise ValueError("TELEGRAM_ALLOWED_USER_ID missing in .env")

print("Bot starting...")
print(f"Allowed user id configured: {ALLOWED_USER_ID}")

bot = Bot(token=TOKEN)
dp = Dispatcher()


def is_authorized(message: types.Message) -> bool:
    user_id = message.from_user.id if message.from_user else None
    return str(user_id) == ALLOWED_USER_ID


@dp.message(CommandStart())
async def start_handler(message: types.Message):
    print("Received /start command")
    print(f"Sender user id: {message.from_user.id}")

    if not is_authorized(message):
        print("Unauthorized user blocked")
        return

    print("Authorized user, sending response")
    await message.answer("Agent online.")


@dp.message()
async def capture_message(message: types.Message):
    user_id = message.from_user.id if message.from_user else None

    print("Received message")
    print(f"Sender user id: {user_id}")

    if not is_authorized(message):
        print("Unauthorized user blocked")
        return

    text = message.text or "[non-text message]"
    print(f"Captured text: {text}")

    # Store in database
    insert_item(text)

    await message.answer("Captured.")


async def main():
    print("Initializing database...")
    init_db()

    print("Polling started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
