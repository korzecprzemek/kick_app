#entrypoint streamlit run
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")
from ui.main import run

if __name__ == "__main__":
    run()