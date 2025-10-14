from database import SessionLocal
from models import PresetSession

db = SessionLocal()


# DB 시드 함수
def seed_sessions():
    db = SessionLocal()
    if not db.query(PresetSession).first():  # 이미 있으면 스킵
        sessions = [
            PresetSession(type_id=1, goal="diverge", duration=25),
            PresetSession(type_id=2, goal="converge", duration=25),
            PresetSession(type_id=3, goal="observe", duration=25),
            PresetSession(type_id=4, goal="screening", duration=25),
            PresetSession(type_id=5, goal="refine", duration=25),
            PresetSession(type_id=6, goal="reverse", duration=25),
            PresetSession(type_id=7, goal="constraint", duration=25),
            PresetSession(type_id=8, goal="emotion", duration=25),
            PresetSession(type_id=9, goal="tagging", duration=25),
            PresetSession(type_id=10, goal="structuring", duration=25),
            PresetSession(type_id=11, goal="analysis", duration=25),
            PresetSession(type_id=12, goal="ruleBreaking", duration=25),
            PresetSession(type_id=13, goal="transformation", duration=25),
            PresetSession(type_id=14, goal="break", duration=5),
            PresetSession(type_id=15, goal="detox", duration=25),
        ]
        db.add_all(sessions)
        db.commit()
    db.close()