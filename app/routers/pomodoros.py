# Pomodoro 생성 / 조회 / 수정 / 삭제

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.schemas import PomodoroCreate, PomodoroOut

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
