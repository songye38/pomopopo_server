from app.db.database import SessionLocal
from app.db.models import PresetPomodoro, PresetSession, PresetPomodoroSession

db = SessionLocal()

def seed_sessions():
    db = SessionLocal()

    # ⚡ 프리셋별 세션 순서 정의
    preset_orders = {
        "refine": [1,14,3,14,4,15],
        "reverse": [2,14,3,14,6,15],
        "random": [1,14,7,14,1,15],
        "emotion": [1,14,8,14,1,15],
        "explore": [1,14,9,14,1,15],
        "story": [2,14,10,14,2,15],
        "echo": [3,14,11,14,3,15],
        "escape": [1,14,12,14,1,15],
        "repeat": [1,14,2,14,13,15],
        "empty": [1,14,3,14,1,15],
    }

    try:
        for preset_name, order_sequence in preset_orders.items():
            # 1️⃣ 프리셋 가져오기
            preset = db.query(PresetPomodoro).filter_by(title=preset_name).first()
            if not preset:
                print(f"❌ '{preset_name}' 프리셋을 찾을 수 없습니다. 건너뜁니다.")
                continue

            # 2️⃣ 기존 연결 삭제
            db.query(PresetPomodoroSession).filter_by(preset_id=preset.id).delete()

            # 3️⃣ 새로운 연결 생성
            for order_index, session_id in enumerate(order_sequence, start=1):
                session = db.query(PresetSession).filter_by(id=session_id).first()
                if not session:
                    print(f"⚠️ 세션 id {session_id}을(를) 찾을 수 없어 건너뜁니다.")
                    continue

                db.add(
                    PresetPomodoroSession(
                        preset_id=preset.id,
                        session_id=session.id,
                        order=order_index
                    )
                )

        db.commit()
        print("✅ 모든 프리셋 세션 연결 완료!")

    except Exception as e:
        db.rollback()
        print(f"🚨 오류 발생: {e}")

    finally:
        db.close()
