# pydantic 모델 정의
# 이 파일은 사용자 생성 및 출력 모델을 정의합니다.
# Pydantic은 데이터 유효성 검사 및 설정 관리를 위한 라이브러리
# FastAPI와 함께 사용되어 API 요청 및 응답의 데이터 구조를 정의합니다.

import uuid
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# -----------------------------
# User 관련 스키마
# -----------------------------
class UserCreate(BaseModel):
    email: str
    password: str
    name: str

class UserOut(BaseModel):
    id: uuid.UUID
    email: str
    name: str

    model_config = {"from_attributes": True}


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str
    user: UserOut


# -----------------------------
# Session 스키마
# -----------------------------
class SessionCreate(BaseModel):
    type_id: int
    goal: str
    duration: int
    order: int
    name : str #새로 추가



class SessionOut(BaseModel):
    id : int
    type_id: int
    goal: str
    duration: int
    order: int
    name : str #새로 추가

    model_config = {"from_attributes": True}


# 세션 업데이트용
class SessionUpdate(BaseModel):
    id: Optional[uuid.UUID]  # 기존 세션이면 id, 새로 추가되는 세션이면 None
    type_id: int
    goal: str
    duration: int
    order: int
    name: str



# -----------------------------
# Pomodoro 스키마
# -----------------------------
class PomodoroCreate(BaseModel):
    title: str
    sessions: List[SessionCreate]

class PomodoroOut(BaseModel):
    id: uuid.UUID
    title: str
    sessions: List[SessionOut] = []
    
    class Config:
        orm_mode = True  # ORM 객체를 바로 Pydantic 모델로 변환 가능

# 뽀모도로 업데이트용
class PomodoroUpdate(BaseModel):
    title: Optional[str] = None
    sessions: Optional[List[SessionUpdate]] = []

    class Config:
        orm_mode = True



class StartPomodoroRequest(BaseModel):
    pomodoro_id: uuid.UUID


class FinishSessionRequest(BaseModel):
    session_log_id: int
    total_paused_duration: int
    pause_count: int

class FinishPomodoroRequest(BaseModel):
    log_id: uuid.UUID


class UserStatsResponse(BaseModel):
    user_id: uuid.UUID
    total_pomodoros: int
    total_sessions: int
    total_focus_duration_minutes: int
    average_focus_rate: int
    last_active_at: Optional[datetime]