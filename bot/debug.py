import asyncio
from services.lms_client import fetch_items, fetch_pass_rates

async def main():
    items = await fetch_items()
    print("=== ПЕРВЫЙ ЭЛЕМЕНТ ИЗ /items/ ===")
    print(items[0] if items else "Пусто!")
    
    rates = await fetch_pass_rates("lab-04")
    print("\n=== СЫРЫЕ ОЦЕНКИ ИЗ /pass-rates?lab=lab-04 ===")
    print(rates)

asyncio.run(main())
