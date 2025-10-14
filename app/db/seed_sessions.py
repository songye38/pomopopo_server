from app.db.database import SessionLocal
from app.db.models import PresetPomodoro,Session

db = SessionLocal()


# DB 시드 함수
def seed_sessions():
    db = SessionLocal()
    presets = [
        PresetPomodoro(title="refine"),
        PresetPomodoro(title="reverse"),
        PresetPomodoro(title="random"),
        PresetPomodoro(title="emotion"),
        PresetPomodoro(title="explore"),
        PresetPomodoro(title="story"),
        PresetPomodoro(title="echo"),
        PresetPomodoro(title="escape"),
        PresetPomodoro(title="repeat"),
        PresetPomodoro(title="empty")
    ]
    db.add_all(presets)
    db.commit()
    db.close()