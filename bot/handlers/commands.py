import httpx
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from services.lms_client import fetch_items, fetch_pass_rates
from services.llm_router import process_natural_language

def get_start_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📚 What labs are available?", callback_data="llm_ask_labs")],
        [InlineKeyboardButton(text="📊 Top learners in Lab 04", callback_data="llm_ask_top")]
    ])

async def handle_start(is_telegram=False):
    text = "Welcome to the AI-powered LMS Bot! 🚀\nUse commands or just ask me anything in plain text!"
    if is_telegram: return text, get_start_keyboard()
    return text

# ... (Остальные команды оставляем без изменений для обратной совместимости)
async def handle_help() -> str:
    return "/start - Welcome\n/help - Commands\n/health - Backend status\n/labs - List labs\n/scores <lab> - Pass rates"

async def handle_health() -> str:
    try:
        items = await fetch_items()
        return f"Backend is healthy. {len(items)} items available."
    except Exception as e: return f"Backend error: {e}"

async def handle_labs() -> str:
    try:
        items = await fetch_items()
        labs = {item["title"] for item in items if isinstance(item, dict) and item.get("type") == "lab" and item.get("title")}
        return "Available labs:\n" + "\n".join(f"- {lab}" for lab in sorted(labs)) if labs else "No labs found."
    except Exception as e: return f"Backend error: {e}"

async def handle_scores(command: str) -> str:
    parts = command.strip().split()
    if len(parts) < 2: return "Please provide a lab ID. Example: /scores lab-04"
    try:
        rates = await fetch_pass_rates(parts[1])
        if not rates: return "No data."
        res = f"Pass rates for {parts[1]}:\n"
        if isinstance(rates, list):
            for item in rates:
                task = item.get("task", "Unknown Task")
                score = item.get("avg_score", 0)
                res += f"- {task}: {float(score):.1f}%\n"
        return res.strip()
    except Exception as e: return f"Backend error: {e}"

# НОВАЯ ФУНКЦИЯ: Обработка свободного текста
async def handle_natural_language(text: str) -> str:
    return await process_natural_language(text)
