# OAuth, tokens, refreshing
import os
import requests
import secrets
import base64
import hashlib
import urllib.parse

OAUTH_HOST = "https://id.kick.com"
AUTHORIZE_URL = f"{OAUTH_HOST}/oauth/authorize"
TOKEN_URL = f"{OAUTH_HOST}/oauth/token"

def _base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")

def generate_pkce_pair():
    code_verifier = secrets.token_urlsafe(64)
    digest = hashlib.sha256(code_verifier.encode("ascii")).digest()
    code_challenge = _base64url_encode(digest)
    return code_verifier,code_challenge

def build_authorize_url():
    client_id = os.getenv("KICK_CLIENT_ID")
    redirect_uri = os.getenv("KICK_REDIRECT_URI")
    scope = "user:read channel:read"

    if not client_id or not redirect_uri:
        raise RuntimeError("Brakuje KICK_CLIENT albo KICK_REDIRECT_URI w env")
    
    state = secrets.token_urlsafe(16)
    code_verifier, code_challenge = generate_pkce_pair()
    params = {
        "client_id":client_id,
        "redirect_uri":redirect_uri,
        "response_type": "code",
        "scope": scope,
        "state": state,
        "code_challenge":code_challenge,
        "code_challenge_method":"S256"
    }
    url = AUTHORIZE_URL + "?" + urllib.parse.urlencode(params)
    return url, code_verifier, state

def exchange_code_for_token(code: str, code_verifier: str) -> dict:
    client_id = os.getenv("KICK_CLIENT_ID")
    client_secret = os.getenv("KICK_CLIENT_SECRET")
    redirect_uri = os.getenv("KICK_REDIRECT_URI")

    if not client_id or not client_secret or not redirect_uri:
        raise RuntimeError("Brakuje KICK_CLIENT_ID / KICK_CLIENT_SECRET / KICK_REDIRECT_URI")
    
    data = {
        "grant_type":"authorization_code",
        "code":code,
        "client_id":client_id,
        "client_secret":client_secret,
        "redirect_uri":redirect_uri,
        "code_verifier":code_verifier
    }

    r = requests.post(
        TOKEN_URL,
        data = data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=20
    )

    try:
        payload = r.json()
    except Exception:
        payload = {"raw":r.text}

    if not r.ok:
        raise RuntimeError(f"Token exchange failed: {r.status_code} {payload}")
    return payload

def refresh_access_token(refresh_token: str) -> dict:
    client_id = os.getenv("KICK_CLIENT_ID")
    client_secret = os.getenv("KICK_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise RuntimeError("Brakuje KICK_CLIENT_ID albo KICK_CLIENT_SECRET w env")

    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret,
    }

    r = requests.post(
        TOKEN_URL,
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=20,
    )

    try:
        payload = r.json()
    except Exception:
        payload = {"raw": r.text}

    if not r.ok:
        raise RuntimeError(f"Refresh failed: {r.status_code} {payload}")

    return payload

