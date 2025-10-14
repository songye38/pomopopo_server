# Pomodoro 생성 / 조회 / 수정 / 삭제

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.db import models
from app.db.database import get_db

router = APIRouter(prefix="/pomodoros", tags=["pomodoros"])

# --------------------------
# Pomodoro 생성
# --------------------------
@router.post("/")
def create_pomodoro(pomodoro_data: dict, db: Session = Depends(get_db)):
    """
    pomodoro_data 예시:
    {
        "title": "집중 공부",
        "user_id": "uuid-string"
    }
    """
    # user 존재 여부 확인
    user = db.query(models.User).filter(models.User.id == pomodoro_data["user_id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    pomodoro = models.Pomodoro(**pomodoro_data)
    db.add(pomodoro)
    db.commit()
    db.refresh(pomodoro)
    return pomodoro


# --------------------------
# 특정 Pomodoro 조회
# --------------------------
@router.get("/{pomodoro_id}")
def get_pomodoro(pomodoro_id: UUID, db: Session = Depends(get_db)):
    pomodoro = db.query(models.Pomodoro).filter(models.Pomodoro.id == pomodoro_id).first()
    if not pomodoro:
        raise HTTPException(status_code=404, detail="Pomodoro not found")
    return pomodoro


# --------------------------
# 사용자의 모든 Pomodoro 조회
# --------------------------
@router.get("/user/{user_id}")
def get_user_pomodoros(user_id: UUID, db: Session = Depends(get_db)):
    pomodoros = db.query(models.Pomodoro).filter(models.Pomodoro.user_id == user_id).all()
    return pomodoros


# --------------------------
# Pomodoro 수정
# --------------------------
@router.put("/{pomodoro_id}")
def update_pomodoro(pomodoro_id: UUID, update_data: dict, db: Session = Depends(get_db)):
    pomodoro = db.query(models.Pomodoro).filter(models.Pomodoro.id == pomodoro_id).first()
    if not pomodoro:
        raise HTTPException(status_code=404, detail="Pomodoro not found")
    
    for key, value in update_data.items():
        setattr(pomodoro, key, value)
    
    db.commit()
    db.refresh(pomodoro)
    return pomodoro


# --------------------------
# Pomodoro 삭제
# --------------------------
@router.delete("/{pomodoro_id}")
def delete_pomodoro(pomodoro_id: UUID, db: Session = Depends(get_db)):
    pomodoro = db.query(models.Pomodoro).filter(models.Pomodoro.id == pomodoro_id).first()
    if not pomodoro:
        raise HTTPException(status_code=404, detail="Pomodoro not found")
    
    db.delete(pomodoro)
    db.commit()
    return {"detail": "Pomodoro deleted"}
