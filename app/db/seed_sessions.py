from app.db.database import SessionLocal
from app.db.models import PresetPomodoro, PresetSession, PresetPomodoroSession

def seed_sessions():
    db = SessionLocal()
    try:
        preset = db.query(PresetPomodoro).filter_by(title="refine").first()
        if not preset:
            raise ValueError("❌ 'refine' 프리셋을 찾을 수 없습니다.")

        db.query(PresetPomodoroSession).filter_by(preset_id=preset.id).delete()

        order_sequence = [1, 14, 3, 14, 5, 15]  # ← 세션 id 순서

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
        print("✅ 'refine' 프리셋 세션 연결 완료!")

    except Exception as e:
        db.rollback()
        print(f"🚨 오류 발생: {e}")

    finally:
        db.close()
