import argparse
import asyncio
import sys
import logging
import socket
import aiohttp
from aiogram.client.session.aiohttp import AiohttpSession

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

from handlers.commands import handle_start, handle_help, handle_health, handle_labs, handle_scores

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

async def async_run_test_mode(command: str):
    cmd = command.strip()
    if cmd.startswith("/start"): print(await handle_start())
    elif cmd.startswith("/help"): print(await handle_help())
    elif cmd.startswith("/health"): print(await handle_health())
    elif cmd.startswith("/labs"): print(await handle_labs())
    elif cmd.startswith("/scores"): print(await handle_scores(cmd))
    else: print("Unknown command. Please use /help.")
    sys.exit(0)

async def start_telegram_bot():
    from aiogram import Bot, Dispatcher
    from aiogram.filters import CommandStart, Command
    from aiogram.types import Message
    from config import BOT_TOKEN

    if not BOT_TOKEN:
        logging.error("BOT_TOKEN is missing!")
        sys.exit(1)

    session = CustomSession()
    bot = Bot(token=BOT_TOKEN, session=session)
    dp = Dispatcher()

    @dp.message(CommandStart())
    async def cmd_start(message: Message): await message.answer(await handle_start())

    @dp.message(Command("help"))
    async def cmd_help(message: Message): await message.answer(await handle_help())

    @dp.message(Command("health"))
    async def cmd_health(message: Message): await message.answer(await handle_health())

    @dp.message(Command("labs"))
    async def cmd_labs(message: Message): await message.answer(await handle_labs())

    @dp.message(Command("scores"))
    async def cmd_scores(message: Message): await message.answer(await handle_scores(message.text))

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
        asyncio.run(async_run_test_mode(args.test))
    else:
        asyncio.run(start_telegram_bot())

if __name__ == "__main__":
    main()
