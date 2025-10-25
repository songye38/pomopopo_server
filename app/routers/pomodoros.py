# Pomodoro 생성 / 조회 / 수정 / 삭제

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.schemas import PomodoroCreate, PomodoroOut
from typing import List
from fastapi import Path
from fastapi import HTTPException

router = APIRouter(prefix="/pomodoros", tags=["pomodoros"])
from app.auth.dependencies import get_current_user
from app.db.models import User, Pomodoro, Session


# --------------------------
# Pomodoro 생성
# --------------------------
@router.post("/add", response_model=PomodoroOut)
async def create_pomodoro(
    data: PomodoroCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 1️⃣ Pomodoro 생성
    pomodoro = Pomodoro(title=data.title, user_id=current_user.id)
    db.add(pomodoro)
    db.commit()
    db.refresh(pomodoro)

    # 2️⃣ Session들 생성
    for s in data.sessions:
        session = Session(
            pomodoro_id=pomodoro.id,
            type_id=s.type_id,
            goal=s.goal,
            duration=s.duration,
            order=s.order,
        )
        db.add(session)

    db.commit()
    db.refresh(pomodoro)

    return pomodoro


# --------------------------
# 특정 사용자 뽀모도로 조회
# --------------------------
@router.get("/", response_model=List[PomodoroOut])
async def get_user_pomodoros(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    pomodoros = (
        db.query(Pomodoro)
        .filter(Pomodoro.user_id == current_user.id)
        .all()
    )
    return pomodoros



# --------------------------
# 특정 뽀모도로 조회
# --------------------------
@router.get("/{pomodoro_id}", response_model=PomodoroOut)
async def get_pomodoro_by_id(
    pomodoro_id: str = Path(..., description="조회할 뽀모도로 ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    pomodoro = (
        db.query(Pomodoro)
        .filter(Pomodoro.user_id == current_user.id, Pomodoro.id == pomodoro_id)
        .first()
    )
    if not pomodoro:
        raise HTTPException(status_code=404, detail="뽀모도로를 찾을 수 없습니다")
    
    return pomodoro


# --------------------------
# 특정 뽀모도로 삭제
# --------------------------
@router.delete("/{pomodoro_id}", response_model=dict)
async def delete_pomodoro(
    pomodoro_id: str = Path(..., description="삭제할 뽀모도로 ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 1️⃣ 뽀모도로 조회
    pomodoro = db.query(Pomodoro).filter(
        Pomodoro.user_id == current_user.id, Pomodoro.id == pomodoro_id
    ).first()

    if not pomodoro:
        raise HTTPException(status_code=404, detail="삭제할 뽀모도로를 찾을 수 없습니다")

    # 2️⃣ 연관된 세션 삭제
    db.query(Session).filter(Session.pomodoro_id == pomodoro.id).delete()

    # 3️⃣ 뽀모도로 삭제
    db.delete(pomodoro)
    db.commit()

    return {"message": "뽀모도로가 성공적으로 삭제되었습니다."}