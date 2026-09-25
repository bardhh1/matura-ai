import os
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))
os.chdir(BACKEND_DIR)

from app.config import get_settings
from app.db.session import create_database
from app.seed_data import seed_demo_content


def seed() -> None:
    database = create_database(get_settings().database_url)
    with database.session_factory() as session:
        total = seed_demo_content(session)
        print(f"Seeded 6 subjects, 18 skills, {total} questions.")
    database.engine.dispose()


if __name__ == "__main__":
    seed()
