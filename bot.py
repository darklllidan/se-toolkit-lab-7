import argparse, asyncio, sys, logging, socket, aiohttp, os, traceback
from aiogram.client.session.aiohttp import AiohttpSession

# Жесткая привязка путей для импортов
sys.path.append(os.path.dirname(__file__))

from handlers.commands import handle_start, handle_help, handle_health, handle_labs, handle_scores, handle_natural_language

logging.basicConfig(level=logging.ERROR) # Уменьшим шум в логах

class CustomSession(AiohttpSession):
    async def create_session(self) -> aiohttp.ClientSession:
        if self._session is None:
            self._session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(family=socket.AF_INET), trust_env=True)
        return self._session

async def async_run_test_mode(command: str):
    try:
        cmd = command.strip()
        if cmd.startswith("/start"): print(await handle_start(False))
        elif cmd.startswith("/help"): print(await handle_help())
        elif cmd.startswith("/health"): print(await handle_health())
        elif cmd.startswith("/labs"): print(await handle_labs())
        elif cmd.startswith("/scores"): print(await handle_scores(cmd))
        else:
            # Вызов LLM роутера
            response = await handle_natural_language(cmd)
            print(response)
        sys.exit(0)
    except Exception:
        traceback.print_exc()
        sys.exit(1)

async def start_telegram_bot():
    from aiogram import Bot, Dispatcher, F
    from aiogram.filters import CommandStart, Command
    from aiogram.types import Message, CallbackQuery
    import config

    bot = Bot(token=config.BOT_TOKEN, session=CustomSession())
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

    @dp.callback_query(F.data.startswith("llm_ask_"))
    async def handle_buttons(callback: CallbackQuery):
        query = "What labs are available?" if callback.data == "llm_ask_labs" else "Who are the top learners in lab 04?"
        await callback.message.answer(await handle_natural_language(query))
        await callback.answer()

    @dp.message(F.text & ~F.text.startswith('/'))
    async def handle_text(message: Message):
        await message.answer(await handle_natural_language(message.text))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", type=str)
    args = parser.parse_args()
    if args.test:
        asyncio.run(async_run_test_mode(args.test))
    else:
        asyncio.run(start_telegram_bot())

if __name__ == "__main__":
    main()
