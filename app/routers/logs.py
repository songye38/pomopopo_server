from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from uuid import UUID
from sqlalchemy import func

from app.db.database import get_db
from app.auth.dependencies import get_current_user
from app.db.models import User, UserPomodoroLog, SessionLog, Session

router = APIRouter(prefix="/logs", tags=["logs"])

# --------------------------
# 1️⃣ 뽀모도로 시작
# --------------------------
@router.post("/pomodoro/start")
def start_pomodoro(
    pomodoro_id: UUID = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """새로운 뽀모도로 로그 생성 및 id 반환"""
    log = UserPomodoroLog(
        user_id=current_user.id,
        pomodoro_id=pomodoro_id,
        started_at=datetime.utcnow(),
        completed=False
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return {"log_id": log.id, "success": True}


# --------------------------
# 2️⃣ 세션 로그 추가
# --------------------------
@router.post("/session/add")
def add_session_log(
    log_id: UUID,
    session_id: int = None,
    goal: str = None,
    duration: int = None,
    order: int = None,
    db: Session = Depends(get_db)
):
    """세션 로그 기록"""
    if not (session_id):
        raise HTTPException(status_code=400, detail="session_id 또는 preset_session_id 중 하나는 필수입니다.")

    s_log = SessionLog(
        log_id=log_id,
        session_id=session_id,
        goal=goal or "",
        duration=duration,
        order=order,
        started_at=datetime.utcnow(),
        completed=False,
        pause_count=0,              # 초기값
        total_paused_duration=0     # 초기값
        
    )
    db.add(s_log)
    db.commit()
    db.refresh(s_log)
    return {"session_log_id": s_log.id, "success": True}


# --------------------------
# 3️⃣ 세션 로그 완료 처리
# --------------------------
@router.patch("/session/finish")
def finish_session_log(
    session_log_id: int,
    total_paused_duration: int = 0,  # 프론트에서 계산해서 전달
    pause_count: int = 0,            # 프론트에서 계산해서 전달
    db: Session = Depends(get_db)
):
    s_log = db.query(SessionLog).get(session_log_id)
    if not s_log:
        raise HTTPException(status_code=404, detail="Session log not found")
    
    s_log.finished_at = datetime.utcnow()
    s_log.completed = True
    s_log.total_paused_duration = total_paused_duration
    s_log.pause_count = pause_count
    
    db.commit()
    return {"session_log_id": s_log.id, "completed": True}


# --------------------------
# 4️⃣ 뽀모도로 종료
# --------------------------
@router.post("/pomodoro/finish")
def finish_pomodoro(
    log_id: UUID,
    db: Session = Depends(get_db)
):
    """뽀모도로 로그 완료 처리"""
    log = db.query(UserPomodoroLog).get(log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Pomodoro log not found")

    log.finished_at = datetime.utcnow()
    # 총 세션 시간 합산
    total_duration = db.query(func.sum(SessionLog.duration)).filter(SessionLog.log_id==log_id).scalar()
    log.total_duration = total_duration or 0
    log.completed = True
    db.commit()
    return {"log_id": log.id, "completed": True, "total_duration": log.total_duration}
