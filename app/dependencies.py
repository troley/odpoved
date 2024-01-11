from app.db.database import SessionLocal
from app.ai.llm import LLM


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_llm():
    yield LLM
