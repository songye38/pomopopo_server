from app.db.database import SessionLocal
from app.db.models import PresetPomodoro, PresetSession, PresetPomodoroSession

db = SessionLocal()

def seed_sessions():
    # 예: refine 프리셋의 연결 세션 삭제
    db.query(PresetPomodoroSession).filter_by(preset_id=1).delete()
    db.commit()
    db.close()
    # db = SessionLocal()
    # try:
    #     preset = db.query(PresetPomodoro).filter_by(title="random").first()
    #     if not preset:
    #         raise ValueError("❌ 'random' 프리셋을 찾을 수 없습니다.")

    #     db.query(PresetPomodoroSession).filter_by(preset_id=preset.id).delete()

    #     order_sequence = [0,13,6,13,0,14]  # ← 세션 id 순서

    #     for order_index, session_id in enumerate(order_sequence, start=1):
    #         session = db.query(PresetSession).filter_by(id=session_id).first()
    #         if not session:
    #             print(f"⚠️ 세션 id {session_id}을(를) 찾을 수 없어 건너뜁니다.")
    #             continue

    #         db.add(
    #             PresetPomodoroSession(
    #                 preset_id=preset.id,
    #                 session_id=session.id,
    #                 order=order_index
    #             )
    #         )

    #     db.commit()
    #     print("✅ 'random' 프리셋 세션 연결 완료!")

    # except Exception as e:
    #     db.rollback()
    #     print(f"🚨 오류 발생: {e}")

    # finally:
    #     db.close()
