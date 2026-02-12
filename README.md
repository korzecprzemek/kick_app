# PeekKick 

Prosta aplikacja w **Python + Streamlit** do przeglądania danych z Kick API.  
Logowanie przez **OAuth2 + PKCE**.

##  Funkcje
- Logowanie przez Kick (OAuth2 + PKCE)
- Pobranie access_token + refresh_token
- Podstawowe zapytania do Kick API (np. profil zalogowanego użytkownika)
- Prosty interfejs w Streamlit

##  Struktura projektu
```text
├── kick_client
│   ├── __init__.py
│   ├── auth.py
│   ├── data.py
│   └── errors.py
├── main.py
├── models
│   ├── __init__.py
│   ├── stream.py
│   └── user.py
├── requirements.txt
├── tree.txt
└── ui
    ├── __init__.py
    └── main.py
```

## Wymagania
- Python 3.9+
- Konto developerskie Kick (Client ID + Client Secret)
```bash
pip install requirements.txt
```

## Konfiguracja

W głównym katalogu projektu utwórz `.env`:
- KICK_CLIENT_ID = ...
- KICK_CLIENT_SECRET = ...
- KICK_REDIRECT_URI = http://localhost:8501

## Uruchomienie
```bash
streamlit run main.py
```

## Roadmap
- wyszukiwanie użytkowników/kanałów po nazwie
- wykresy statystyk streamerów
- cache zapytań do API

Projekt edukacyjny, devowy.


