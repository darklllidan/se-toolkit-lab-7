import httpx
from config import LMS_API_BASE_URL, LMS_API_KEY

def get_headers():
    return {"Authorization": f"Bearer {LMS_API_KEY}"} if LMS_API_KEY else {}

async def fetch_json(url: str, params=None):
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params, headers=get_headers())
        resp.raise_for_status()
        return resp.json()

async def fetch_items(): return await fetch_json(f"{LMS_API_BASE_URL}/items/")
async def fetch_learners(): return await fetch_json(f"{LMS_API_BASE_URL}/learners/")
async def fetch_scores(lab: str): return await fetch_json(f"{LMS_API_BASE_URL}/analytics/scores", {"lab": lab})
async def fetch_pass_rates(lab: str): return await fetch_json(f"{LMS_API_BASE_URL}/analytics/pass-rates", {"lab": lab})
async def fetch_timeline(lab: str): return await fetch_json(f"{LMS_API_BASE_URL}/analytics/timeline", {"lab": lab})
async def fetch_groups(lab: str): return await fetch_json(f"{LMS_API_BASE_URL}/analytics/groups", {"lab": lab})
async def fetch_top_learners(lab: str, limit: int = 5): return await fetch_json(f"{LMS_API_BASE_URL}/analytics/top-learners", {"lab": lab, "limit": limit})
async def fetch_completion_rate(lab: str): return await fetch_json(f"{LMS_API_BASE_URL}/analytics/completion-rate", {"lab": lab})

async def trigger_sync():
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{LMS_API_BASE_URL}/pipeline/sync", headers=get_headers(), json={})
        resp.raise_for_status()
        return resp.json()
