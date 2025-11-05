from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy import func,desc
from datetime import datetime
from uuid import UUID

from app.db.database import get_db
from app.auth.dependencies import get_current_user
from app.db.models import User, UserPomodoroLog, SessionLog, Session, SessionStatus,UserStats
from app.db.schemas import StartPomodoroRequest, FinishSessionRequest,FinishPomodoroRequest,UserStatsResponse

router = APIRouter(prefix="/logs", tags=["logs"])


# --------------------------
# 1️⃣ 뽀모도로 시작
# --------------------------
@router.post("/pomodoro/start")
def start_pomodoro(
    request: StartPomodoroRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """새 뽀모도로 세션 시작"""
    log = UserPomodoroLog(
        user_id=current_user.id,
        pomodoro_id=request.pomodoro_id,
        started_at=datetime.utcnow(),
        status=SessionStatus.NOT_STARTED,
        completed=False,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return {"log_id": log.id, "success": True}


# --------------------------
# 2️⃣ 세션 로그 생성
# --------------------------
@router.post("/session/add")
def add_session_log(
    log_id: UUID = Body(...),
    session_id: int = Body(...),
    goal: str = Body(None),
    planned_duration: int = Body(...),
    order: int = Body(None),
    db: Session = Depends(get_db),
):
    """뽀모도로 내 세션 시작 로그 추가"""
    s_log = SessionLog(
        log_id=log_id,
        session_id=session_id,
        goal=goal or "",
        planned_duration=planned_duration,
        order=order,
        started_at=datetime.utcnow(),
        status=SessionStatus.NOT_STARTED,
        completed=False,
    )

    db.add(s_log)
    db.commit()
    db.refresh(s_log)
    return {"session_log_id": s_log.id, "success": True}


# --------------------------
# 3️⃣ 세션 완료 처리
# --------------------------
@router.patch("/session/finish")
def finish_session_log(
    body: FinishSessionRequest,
    db: Session = Depends(get_db),
):
    """개별 세션 종료 및 시간 계산"""
    s_log = db.query(SessionLog).get(body.session_log_id)
    if not s_log:
        raise HTTPException(status_code=404, detail="Session log not found")

    # 세션 종료 시간 및 상태 갱신
    s_log.finished_at = datetime.utcnow()
    s_log.total_paused_duration = body.total_paused_duration or 0
    s_log.status = SessionStatus.COMPLETED
    s_log.completed = True

    # duration 계산 자동 반영 (before_flush 훅에서)
    db.commit()

    return {
        "session_log_id": s_log.id,
        "effective_duration": s_log.effective_duration,
        "focus_rate": s_log.focus_rate,
        "completed": True,
    }


# --------------------------
# 4️⃣ 뽀모도로 종료 처리
# --------------------------
@router.post("/pomodoro/finish")
def finish_pomodoro(
    body: FinishPomodoroRequest,  # ✅ JSON body { "log_id": "..." } 형식으로 받음
    db: Session = Depends(get_db),
):
    """전체 뽀모도로 종료 및 통계 반영"""
    log = db.query(UserPomodoroLog).get(body.log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Pomodoro log not found")

    # ✅ 종료 시각 및 상태 업데이트
    log.finished_at = datetime.utcnow()
    log.status = SessionStatus.COMPLETED
    log.completed = True

    # ✅ 총 집중 시간 계산 (effective_duration 기준)
    total_effective = (
        db.query(func.sum(SessionLog.effective_duration))
        .filter(SessionLog.log_id == body.log_id)
        .scalar()
        or 0
    )
    log.total_effective_duration = total_effective

    db.commit()

    return {
        "log_id": str(log.id),
        "completed": True,
        "total_effective_duration": log.total_effective_duration,
    }


# --------------------------
# 5️⃣ 이번 뽀모도로 정보 요약
# --------------------------
@router.get("/pomodoro/{log_id}/summary")
def get_pomodoro_summary(log_id: UUID, db: Session = Depends(get_db)):
    """
    회고용 요약 데이터를 반환
    :param log_id: UserPomodoroLog.id (UUID)
    """
    # DB에서 PK 컬럼명이 id라면 id로 조회해야 함
    log = db.query(UserPomodoroLog).filter(UserPomodoroLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Pomodoro log not found")

    sessions = db.query(SessionLog).filter(SessionLog.log_id == log.id).all()
    total_sessions = len(sessions)
    total_time = sum((s.effective_duration or 0) for s in sessions)
    total_planned = sum((s.planned_duration or 0) for s in sessions) or 1  # 0으로 나누는 것 방지
    focus_rate = int((total_time / total_planned) * 100)

    return {
        "total_sessions": total_sessions,
        "total_minutes": total_time // 60,
        "focus_rate": focus_rate,
        "comment": log.comment,
        "rating": log.rating,
    }


# --------------------------
# 6️⃣ 피드백 저장하는 라우터
# --------------------------
@router.patch("/pomodoro/{log_id}/feedback")
def update_pomodoro_feedback(
    log_id: UUID,
    body: dict = Body(...),
    db: Session = Depends(get_db)
):
    log = db.query(UserPomodoroLog).get(log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")

    log.comment = body.get("comment", log.comment)
    log.rating = body.get("rating", log.rating)
    db.commit()
    return {"success": True}



# --------------------------
# 7️⃣ 로그인 유저 통계 조회
# --------------------------
@router.get("/user/me/stats", response_model=UserStatsResponse)
def get_my_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """로그인한 유저의 뽀모도로 통계 조회"""
    stats = db.query(UserStats).filter(UserStats.user_id == current_user.id).first()
    if not stats:
        raise HTTPException(status_code=404, detail="User stats not found")
    
    return UserStatsResponse(
        user_id=stats.user_id,
        total_pomodoros=stats.total_pomodoros,
        total_sessions=stats.total_sessions,
        total_focus_duration_minutes=stats.total_focus_duration // 60,
        average_focus_rate=stats.average_focus_rate,
        last_active_at=stats.last_active_at,
    )
