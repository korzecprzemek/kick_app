#endpoints calls (profiles, streams, etc.)
import requests
from typing import Optional, Dict, Any
API_BASE = "https://api.kick.com/public/v1"

def _get(path: str,
        access_token: str,
        params: Optional[Dict[str,Any]] = None 
        ) -> dict:
    r = requests.get(
        f"{API_BASE}{path}",
        headers={"Authorization": f"Bearer {access_token}"},
        params=params,
        timeout=20,
    )
    r.raise_for_status()
    return r.json()

def get_me(access_token: str) -> dict:
    return _get("/users", access_token)

def get_channels(access_token: str,
                 user_id: Optional[int] = None,
                 slug: Optional[str] = None,
                 is_live: Optional[bool] = None,
                 page: int = 1,
                 limit: int = 20
) -> dict:
    params = {
        "user_id": user_id,
        "slug": slug,
        "is_live": is_live,
        "page": page,
        "limit": limit
    }
    params = {k: v for k, v in params.items() if v is not None}
    return _get("/channels",access_token, params = params)