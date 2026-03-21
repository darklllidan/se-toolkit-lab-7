# Development Plan for LMS Telegram Bot

## Phase 1: Scaffold and Architecture
The goal is to create a testable architecture where business logic (handlers) is completely separated from the Telegram transport layer. We will use a `--test` CLI flag to allow offline testing of command outputs without requiring a valid Telegram bot token or connection. This ensures modularity and easy debugging.

## Phase 2: Backend Integration
In this phase, we will connect the bot to the LMS API. The `services/` directory will contain an HTTP client (using `httpx`) that communicates with the backend (port 42002) using the `LMS_API_KEY` for authorization. Commands like `/health`, `/labs`, and `/scores` will fetch real data instead of static placeholders.

## Phase 3: Intent Routing using LLM
We will integrate the Qwen Code API proxy to parse complex or unstructured user inputs. The LLM will route natural language queries to the appropriate handler or extract required parameters (e.g., parsing a lab number from 'how did I do on the fourth lab?').

## Phase 4: Deployment
The final bot will be deployed on the VM using `nohup` or a systemd service to run persistently. The environment variables will be securely managed via `.env.bot.secret`.
