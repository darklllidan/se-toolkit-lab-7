def handle_start() -> str:
    return "Welcome to the LMS Bot! Type /help to see available commands."

def handle_help() -> str:
    return "Commands: /start, /help, /health, /labs, /scores"

def handle_health() -> str:
    return "Backend status: OK (placeholder)"

def handle_labs() -> str:
    return "Available labs: Lab 1, Lab 2 (placeholder)"

def handle_scores(command: str) -> str:
    return f"Scores for {command}: 100% (placeholder)"
