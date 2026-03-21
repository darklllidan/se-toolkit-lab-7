import os
from dotenv import load_dotenv

load_dotenv("../.env.bot.secret")

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
LMS_API_BASE_URL = os.getenv("LMS_API_BASE_URL", "http://localhost:42002")
LMS_API_KEY = os.getenv("LMS_API_KEY", "")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_API_BASE_URL = os.getenv("LLM_API_BASE_URL", "http://localhost:42005/v1")
