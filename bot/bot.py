import argparse
import asyncio
import sys
import logging
import socket
import aiohttp
from aiogram.client.session.aiohttp import AiohttpSession

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

from handlers.commands import handle_start, handle_help, handle_health, handle_labs, handle_scores

# 🧠 УЛЬТИМАТУМ: Пишем свой класс сессии!
# Переопределяем метод создания aiohttp-сессии, чтобы впихнуть туда ВСЕ нужные настройки:
# 1. family=socket.AF_INET -> форсируем IPv4
# 2. trust_env=True -> заставляем читать скрытые системные прокси (как curl)
class CustomSession(AiohttpSession):
    async def create_session(self) -> aiohttp.ClientSession:
        if self._session is None:
            connector = aiohttp.TCPConnector(family=socket.AF_INET)
            self._session = aiohttp.ClientSession(
                connector=connector,
                trust_env=True,
                json_serialize=self.json_dumps
            )
        return self._session
# -----------------------------------------------------

def run_test_mode(command: str):
    cmd = command.strip()
    if cmd.startswith("/start"): print(handle_start())
    elif cmd.startswith("/help"): print(handle_help())
    elif cmd.startswith("/health"): print(handle_health())
    elif cmd.startswith("/labs"): print(handle_labs())
    elif cmd.startswith("/scores"): print(handle_scores(cmd))
    else: print("Not implemented yet")
    sys.exit(0)

async def start_telegram_bot():
    from aiogram import Bot, Dispatcher
    from aiogram.filters import CommandStart, Command
    from aiogram.types import Message
    from config import BOT_TOKEN

    if not BOT_TOKEN:
        logging.error("BOT_TOKEN is missing!")
        sys.exit(1)

    # Используем нашу хакерскую сессию!
    session = CustomSession()
    bot = Bot(token=BOT_TOKEN, session=session)
    dp = Dispatcher()

    @dp.message(CommandStart())
    async def cmd_start(message: Message): 
        logging.info("Received /start")
        await message.answer(handle_start())

    @dp.message(Command("help"))
    async def cmd_help(message: Message): 
        logging.info("Received /help")
        await message.answer(handle_help())

    logging.info("Telegram bot is running! Press Ctrl+C to stop.")
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Network error: {e}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", type=str, help="Run in test mode")
    args = parser.parse_args()

    if args.test:
        run_test_mode(args.test)
    else:
        asyncio.run(start_telegram_bot())

if __name__ == "__main__":
    main()
