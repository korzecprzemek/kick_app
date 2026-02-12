#endpoints calls (profiles, streams, etc.)
import requests

def get_me(access_token: str) -> dict:
    r = requests.get(
        "https://api.kick.com/public/v1/users",
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=20
    )
    r.raise_for_status()
    return r.json()