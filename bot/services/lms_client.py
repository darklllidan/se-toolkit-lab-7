import httpx
from config import LMS_API_BASE_URL, LMS_API_KEY

def get_headers():
    return {"Authorization": f"Bearer {LMS_API_KEY}"} if LMS_API_KEY else {}

async def fetch_items():
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{LMS_API_BASE_URL}/items/", headers=get_headers())
        resp.raise_for_status()
        return resp.json()

async def fetch_pass_rates(lab: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{LMS_API_BASE_URL}/analytics/pass-rates", params={"lab": lab}, headers=get_headers())
        resp.raise_for_status()
        return resp.json()
