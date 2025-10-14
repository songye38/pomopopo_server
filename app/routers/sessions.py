# Pomodoro 안의 세션 관리.
# CRUD + 순서(order) 관리 필요.


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.db import models
from app.db.database import get_db

router = APIRouter(prefix="/sessions", tags=["sessions"])

# --------------------------
# 세션 생성
# --------------------------
@router.post("/")
def create_session(session_data: dict, db: Session = Depends(get_db)):
    """
    session_data 예시:
    {
        "pomodoro_id": "uuid-string",
        "type_id": 1,
        "goal": "집중 공부 25분",
        "duration": 25,
        "order": 1
    }
    """
    # pomodoro 존재 여부 확인
    pomodoro = db.query(models.Pomodoro).filter(models.Pomodoro.id == session_data["pomodoro_id"]).first()
    if not pomodoro:
        raise HTTPException(status_code=404, detail="Pomodoro not found")

    session = models.Session(**session_data)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


# --------------------------
# 특정 Pomodoro 세션 조회
# --------------------------
@router.get("/pomodoro/{pomodoro_id}")
def get_sessions_by_pomodoro(pomodoro_id: UUID, db: Session = Depends(get_db)):
    sessions = db.query(models.Session).filter(models.Session.pomodoro_id == pomodoro_id).order_by(models.Session.order).all()
    if not sessions:
        raise HTTPException(status_code=404, detail="No sessions found for this Pomodoro")
    return sessions


# --------------------------
# 세션 단일 조회
# --------------------------
@router.get("/{session_id}")
def get_session(session_id: int, db: Session = Depends(get_db)):
    session = db.query(models.Session).filter(models.Session.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


# --------------------------
# 세션 수정
# --------------------------
@router.put("/{session_id}")
def update_session(session_id: int, update_data: dict, db: Session = Depends(get_db)):
    session = db.query(models.Session).filter(models.Session.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    for key, value in update_data.items():
        setattr(session, key, value)
    
    db.commit()
    db.refresh(session)
    return session


# --------------------------
# 세션 삭제
# --------------------------
@router.delete("/{session_id}")
def delete_session(session_id: int, db: Session = Depends(get_db)):
    session = db.query(models.Session).filter(models.Session.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    db.delete(session)
    db.commit()
    return {"detail": "Session deleted"}
