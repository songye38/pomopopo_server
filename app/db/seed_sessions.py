from app.db.database import SessionLocal
from app.db.models import PresetPomodoro,Session

db = SessionLocal()


# DB 시드 함수
def seed_sessions():
    db = SessionLocal()
    presets = [
        PresetPomodoro(title="refine"),
        PresetPomodoro(title="echo"),
        PresetPomodoro(title="reverse"),
        PresetPomodoro(title="constraint"),
        PresetPomodoro(title="emotion"),
        PresetPomodoro(title="observe"),
        PresetPomodoro(title="diverge"),
        PresetPomodoro(title="tagging"),
        PresetPomodoro(title="detox"),
        PresetPomodoro(title="ruleBreaking")
    ]
    db.add_all(presets)
    db.commit()
    db.close()