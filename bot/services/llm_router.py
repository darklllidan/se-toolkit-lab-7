import httpx
import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import config
from services import lms_client

TOOLS = [
    {"type": "function", "function": {"name": "get_items", "description": "Get list of available labs and tasks", "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {"name": "get_learners", "description": "Get enrolled students and groups", "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {"name": "get_scores", "description": "Get score distribution (4 buckets) for a lab", "parameters": {"type": "object", "properties": {"lab": {"type": "string"}}}, "required": ["lab"]}},
    {"type": "function", "function": {"name": "get_pass_rates", "description": "Get per-task average scores and attempt counts for a lab", "parameters": {"type": "object", "properties": {"lab": {"type": "string"}}}, "required": ["lab"]}},
    {"type": "function", "function": {"name": "get_timeline", "description": "Get submissions per day for a lab", "parameters": {"type": "object", "properties": {"lab": {"type": "string"}}}, "required": ["lab"]}},
    {"type": "function", "function": {"name": "get_groups", "description": "Get per-group scores and student counts for a lab", "parameters": {"type": "object", "properties": {"lab": {"type": "string"}}}, "required": ["lab"]}},
    {"type": "function", "function": {"name": "get_top_learners", "description": "Get top N learners by score for a lab", "parameters": {"type": "object", "properties": {"lab": {"type": "string"}, "limit": {"type": "integer"}}}, "required": ["lab"]}},
    {"type": "function", "function": {"name": "get_completion_rate", "description": "Get completion rate percentage for a lab", "parameters": {"type": "object", "properties": {"lab": {"type": "string"}}}, "required": ["lab"]}},
    {"type": "function", "function": {"name": "trigger_sync", "description": "Refresh data from autochecker", "parameters": {"type": "object", "properties": {}}}}
]

async def execute_tool(name: str, args: dict):
    try:
        if name == "get_items": return await lms_client.fetch_items()
        elif name == "get_learners": return await lms_client.fetch_learners()
        elif name == "get_scores": return await lms_client.fetch_scores(args.get("lab"))
        elif name == "get_pass_rates": return await lms_client.fetch_pass_rates(args.get("lab"))
        elif name == "get_timeline": return await lms_client.fetch_timeline(args.get("lab"))
        elif name == "get_groups": return await lms_client.fetch_groups(args.get("lab"))
        elif name == "get_top_learners": return await lms_client.fetch_top_learners(args.get("lab"), args.get("limit", 5))
        elif name == "get_completion_rate": return await lms_client.fetch_completion_rate(args.get("lab"))
        elif name == "trigger_sync": return await lms_client.trigger_sync()
        return {"error": "Unknown tool"}
    except Exception as e:
        return {"error": str(e)}

async def process_natural_language(text: str) -> str:
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Use tools to provide real data. Answer based on tool output."},
        {"role": "user", "content": text}
    ]
    
    model = config.LLM_API_MODEL if config.LLM_API_MODEL else "coder-model"
    headers = {"Authorization": f"Bearer {config.LLM_API_KEY}", "Content-Type": "application/json"}
    
    base_url = str(config.LLM_API_BASE_URL).rstrip('/')
    endpoint = f"{base_url}/chat/completions" if base_url.endswith('/v1') else f"{base_url}/v1/chat/completions"
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            for _ in range(5):
                payload = {"model": model, "messages": messages, "tools": TOOLS}
                resp = await client.post(endpoint, json=payload, headers=headers)
                if resp.status_code != 200:
                    return f"LLM error: HTTP {resp.status_code} - {resp.text}"
                
                data = resp.json()
                msg = data["choices"][0]["message"]
                
                if msg.get("tool_calls"):
                    messages.append(msg)
                    for tc in msg["tool_calls"]:
                        f_name = tc["function"]["name"]
                        try:
                            f_args = json.loads(tc["function"]["arguments"])
                        except Exception as e:
                            f_args = {}
                            
                        print(f"[tool] LLM called: {f_name}({f_args})", file=sys.stderr)
                        res = await execute_tool(f_name, f_args)
                        messages.append({"role": "tool", "tool_call_id": tc["id"], "content": json.dumps(res)})
                    print(f"[summary] Feeding results back to LLM", file=sys.stderr)
                else:
                    return msg.get("content", "No answer generated by LLM.")
            return "Query too complex, stopped after 5 iterations."
    except Exception as e:
        return f"🔥 ROUTER CRASH: {e}"
