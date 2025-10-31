from app.db.database import SessionLocal
from app.db.models import SessionType

db = SessionLocal()

def seed_sessions():
    db = SessionLocal()

    default_types = [
            {"name": "diverge", "description": "발산"},
            {"name": "converge", "description": "수렴"},
            {"name": "observe", "description": "관찰"},
            {"name": "screening", "description": "스크리닝"},
            {"name": "refine", "description": "정밀 조율"},
            {"name": "reverse", "description": "뒤집기 사고"},
            {"name": "constraint", "description": "제약 도입"},
            {"name": "emotion", "description": "감정 기록"},
            {"name": "tagging", "description": "아이디어 태깅"},
            {"name": "structuring", "description": "구조화"},
            {"name": "analysis", "description": "반응 분석"},
            {"name": "ruleBreaking", "description": "규칙 탈착"},
            {"name": "transformation", "description": "변형"},
            {"name": "break", "description": "단기휴식"},
            {"name": "detox", "description": "장기휴식"},
        ]


    try:
        for t in default_types:
            # 중복 체크
            existing = db.query(SessionType).filter_by(name=t["name"]).first()
            if not existing:
                db.add(SessionType(name=t["name"], description=t["description"]))
            db.commit()
            print("✅ 모든 프리셋 세션 연결 완료!")

    except Exception as e:
        db.rollback()
        print(f"🚨 오류 발생: {e}")

    finally:
        db.close()
