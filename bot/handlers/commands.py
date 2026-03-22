import httpx
from services.lms_client import fetch_items, fetch_pass_rates

async def handle_start() -> str:
    return "Welcome to the LMS Bot! 🚀 Use /help to see what I can do."

async def handle_help() -> str:
    return (
        "Available commands:\n"
        "/start - Welcome message\n"
        "/help - Lists all commands\n"
        "/health - Check backend status\n"
        "/labs - List available labs\n"
        "/scores <lab> - Show pass rates for a lab (e.g., /scores lab-04)"
    )

async def handle_health() -> str:
    try:
        items = await fetch_items()
        return f"Backend is healthy. {len(items)} items available."
    except httpx.ConnectError as e:
        return f"Backend error: connection refused ({e}). Check that the services are running."
    except httpx.HTTPStatusError as e:
        return f"Backend error: HTTP {e.response.status_code}. The backend service may be down."
    except Exception as e:
        return f"Backend error: {e}"

async def handle_labs() -> str:
    try:
        items = await fetch_items()
        labs = set()
        for item in items:
            # Ищем четко то, что увидели в дебаге
            if isinstance(item, dict) and item.get("type") == "lab" and item.get("title"):
                labs.add(item["title"])
                
        if not labs:
            return "No labs found in the database. Did you run the ETL sync?"
            
        return "Available labs:\n" + "\n".join(f"- {lab}" for lab in sorted(labs))
    except httpx.ConnectError as e:
        return f"Backend error: connection refused ({e}). Check that the services are running."
    except Exception as e:
        return f"Backend error: {e}"

async def handle_scores(command: str) -> str:
    parts = command.strip().split()
    if len(parts) < 2:
        return "Please provide a lab ID. Example: /scores lab-04"
    lab = parts[1]
    
    try:
        rates = await fetch_pass_rates(lab)
        if not rates:
            return f"No pass rates found for {lab}."
            
        res = f"Pass rates for {lab}:\n"
        
        # Парсим именно тот список словарей, который отдал сервер
        if isinstance(rates, list):
            for item in rates:
                task = item.get("task", "Unknown Task")
                score = item.get("avg_score", 0)
                attempts = item.get("attempts", "")
                att_str = f" ({attempts} attempts)" if attempts else ""
                
                res += f"- {task}: {float(score):.1f}%{att_str}\n"
                
        return res.strip()
    except httpx.ConnectError as e:
        return f"Backend error: connection refused ({e})."
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return f"Lab '{lab}' not found."
        return f"Backend HTTP error: {e.response.status_code}."
    except Exception as e:
        return f"Backend error: {e}"
