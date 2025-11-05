# Pomodoro 생성 / 조회 / 수정 / 삭제

from fastapi import APIRouter, Depends
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.schemas import PomodoroCreate, PomodoroOut,PomodoroUpdate
from typing import List
from fastapi import Path
from fastapi import HTTPException
from uuid import UUID

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
            name = s.name,
        )
        db.add(session)

    db.commit()
    db.refresh(pomodoro)

    return pomodoro


# --------------------------
# 특정 사용자 뽀모도로 조회 (삭제되지 않은 것만)
# --------------------------
@router.get("/", response_model=List[PomodoroOut])
async def get_user_pomodoros(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    pomodoros = (
        db.query(Pomodoro)
        .filter(
            Pomodoro.user_id == current_user.id,
            Pomodoro.is_deleted == False  # ✅ 삭제되지 않은 뽀모도로만
        )
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
    # UUID 유효성 검증
    try:
        pomodoro_uuid = UUID(pomodoro_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="유효하지 않은 UUID입니다")

    # 유저 소유 or 프리셋 둘 중 하나면 허용
    pomodoro = (
        db.query(Pomodoro)
        .filter(
            Pomodoro.id == pomodoro_uuid,
            or_(
                Pomodoro.user_id == current_user.id,
                Pomodoro.is_preset == True
            )
        )
        .first()
    )

    if not pomodoro:
        raise HTTPException(status_code=404, detail="뽀모도로를 찾을 수 없습니다")

    return pomodoro



# --------------------------
# 특정 뽀모도로 수정
# --------------------------

@router.put("/{pomodoro_id}", response_model=PomodoroOut)
async def update_pomodoro(
    pomodoro_id: str = Path(..., description="수정할 뽀모도로 ID"),
    data: PomodoroUpdate = None,  # title + sessions
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if data is None:
        raise HTTPException(status_code=400, detail="수정할 데이터가 필요합니다")

    try:
        pomodoro_uuid = UUID(pomodoro_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="유효하지 않은 UUID입니다")

    pomodoro = (
        db.query(Pomodoro)
        .filter(Pomodoro.user_id == current_user.id, Pomodoro.id == pomodoro_uuid)
        .first()
    )
    if not pomodoro:
        raise HTTPException(status_code=404, detail="뽀모도로를 찾을 수 없습니다")

    # 1️⃣ 뽀모도로 기본 정보 수정
    if data.title is not None:
        pomodoro.title = data.title

    # 2️⃣ 세션 수정
    sessions_to_update = data.sessions or []  # None이면 빈 리스트 처리
    existing_sessions = {s.id: s for s in pomodoro.sessions}  # DB에 있는 세션
    new_session_ids = []

    for s in sessions_to_update:
        if s.id and s.id in existing_sessions:  # 기존 세션 업데이트
            session = existing_sessions[s.id]
            session.type_id = s.type_id
            session.goal = s.goal
            session.duration = s.duration
            session.order = s.order
            session.name = s.name
        else:  # 새로운 세션 추가
            session = Session(
                pomodoro_id=pomodoro.id,
                type_id=s.type_id,
                goal=s.goal,
                duration=s.duration,
                order=s.order,
                name=s.name,
            )
            db.add(session)
        new_session_ids.append(session.id if s.id else None)

    # 3️⃣ DB에는 없는 세션 삭제
    for s in pomodoro.sessions:
        if s.id not in new_session_ids:
            db.delete(s)

    db.commit()
    db.refresh(pomodoro)
    return pomodoro


# --------------------------
# 특정 뽀모도로 삭제 (논리 삭제)
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

    # 2️⃣ 물리 삭제 X → is_deleted = True로 논리 삭제
    pomodoro.is_deleted = True
    db.commit()

    return {"message": "뽀모도로가 성공적으로 삭제 표시되었습니다."}
