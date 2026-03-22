import argparse, asyncio, sys, logging, socket, aiohttp
from aiogram.client.session.aiohttp import AiohttpSession
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

from handlers.commands import handle_start, handle_help, handle_health, handle_labs, handle_scores, handle_natural_language

class CustomSession(AiohttpSession):
    async def create_session(self) -> aiohttp.ClientSession:
        if self._session is None:
            self._session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(family=socket.AF_INET), trust_env=True, json_serialize=self.json_dumps)
        return self._session

async def async_run_test_mode(command: str):
    cmd = command.strip()
    if cmd.startswith("/start"): print(await handle_start(False))
    elif cmd.startswith("/help"): print(await handle_help())
    elif cmd.startswith("/health"): print(await handle_health())
    elif cmd.startswith("/labs"): print(await handle_labs())
    elif cmd.startswith("/scores"): print(await handle_scores(cmd))
    else:
        # Если это не команда - кидаем в LLM!
        print(await handle_natural_language(cmd))
    sys.exit(0)

async def start_telegram_bot():
    from aiogram import Bot, Dispatcher, F
    from aiogram.filters import CommandStart, Command
    from aiogram.types import Message, CallbackQuery
    from config import BOT_TOKEN

    if not BOT_TOKEN:
        logging.error("BOT_TOKEN missing!"); sys.exit(1)

    bot = Bot(token=BOT_TOKEN, session=CustomSession())
    dp = Dispatcher()

    @dp.message(CommandStart())
    async def cmd_start(message: Message): 
        text, kb = await handle_start(True)
        await message.answer(text, reply_markup=kb)

    @dp.message(Command("help"))
    async def cmd_help(message: Message): await message.answer(await handle_help())

    @dp.message(Command("health"))
    async def cmd_health(message: Message): await message.answer(await handle_health())

    @dp.message(Command("labs"))
    async def cmd_labs(message: Message): await message.answer(await handle_labs())

    @dp.message(Command("scores"))
    async def cmd_scores(message: Message): await message.answer(await handle_scores(message.text))

    # Обработка кнопок
    @dp.callback_query(F.data.startswith("llm_ask_"))
    async def handle_buttons(callback: CallbackQuery):
        await callback.message.answer("Thinking... 🧠")
        query = "What labs are available?" if callback.data == "llm_ask_labs" else "Who are the top learners in lab 04?"
        answer = await handle_natural_language(query)
        await callback.message.answer(answer)
        await callback.answer()

    # Перехват любого текста и отправка в LLM
    @dp.message(F.text & ~F.text.startswith('/'))
    async def handle_text(message: Message):
        answer = await handle_natural_language(message.text)
        await message.answer(answer)

    logging.info("Telegram bot is running!")
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as e: logging.error(f"Network error: {e}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", type=str, help="Run in test mode")
    args = parser.parse_args()
    if args.test: asyncio.run(async_run_test_mode(args.test))
    else: asyncio.run(start_telegram_bot())

if __name__ == "__main__": main()
