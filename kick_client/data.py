#endpoints calls (profiles, streams, etc.)
import requests
API_BASE = "https://api.kick.com/public/v1"

def _get(path: str, access_token: str, params: dict | None = None) -> dict:
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
def get_channels(access_token: str, **params) -> dict:
    return _get("/channels",access_token, params = params)