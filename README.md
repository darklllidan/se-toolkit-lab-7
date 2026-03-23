# AI-Powered LMS Bot & Backend 🚀

This repository contains a full-stack educational platform: a FastAPI-based LMS backend and an LLM-powered Telegram bot that acts as an intelligent assistant for learners.

## Features
- **LMS Backend:** RESTful API for managing labs, learners, tasks, and analytics.
- **AI Agent Bot:** Telegram bot powered by Qwen LLM that translates natural language queries into backend API calls (Intent-Based Routing).
- **Dockerized:** Fully containerized architecture using Docker Compose.

---

## 🛠 Deploy

To deploy the bot and the backend database/services using Docker Compose, you need to configure the environment and run the containers.

### 1. Prerequisites (Environment Variables)
Make sure you have a `.env.docker.secret` file in the root directory. It must contain the following required variables:

```env
BOT_TOKEN=8729649755:AAGuJbeUi9qdIMROaDFDCXxALRRo56GX4iQ
LMS_API_KEY=3537
LLM_API_KEY=ygT6aEvtjGJN_BsKOikQF_KXv59nIUAWawdm4-rd0aNjles9TGjikYQZXwTSHE9-WPmh6axoOaBERWMEnhv5tg
LLM_API_MODEL=coder-model
