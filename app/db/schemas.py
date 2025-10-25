# pydantic 모델 정의
# 이 파일은 사용자 생성 및 출력 모델을 정의합니다.
# Pydantic은 데이터 유효성 검사 및 설정 관리를 위한 라이브러리
# FastAPI와 함께 사용되어 API 요청 및 응답의 데이터 구조를 정의합니다.

import uuid
from pydantic import BaseModel, EmailStr
from typing import List, Optional

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
# SessionType 스키마
# -----------------------------
class SessionTypeOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    model_config = {"from_attributes": True}

# -----------------------------
# Session 스키마
# -----------------------------
class SessionCreate(BaseModel):
    type_id: int
    goal: str
    duration: int
    order: int



class SessionOut(BaseModel):
    type: Optional[int] = None  # 없으면 None으로 처리
    goal: str
    duration: int
    order: int

    model_config = {"from_attributes": True}



# -----------------------------
# Pomodoro 스키마
# -----------------------------
class PomodoroCreate(BaseModel):
    title: str
    sessions: List[SessionCreate]

class PomodoroOut(BaseModel):
    id: str
    title: str
    sessions: List[SessionOut] = []
    
    class Config:
        orm_mode = True  # ORM 객체를 바로 Pydantic 모델로 변환 가능


# -----------------------------
# PresetSession 스키마
# -----------------------------
class PresetSessionCreate(BaseModel):
    type_id: int
    goal: str
    duration: int
    order: int

class PresetSessionOut(BaseModel):
    id: int
    type: SessionTypeOut
    goal: str
    duration: int
    order: int

    model_config = {"from_attributes": True}

# -----------------------------
# PresetPomodoro 스키마
# -----------------------------
class PresetPomodoroCreate(BaseModel):
    title: str
    description: Optional[str] = None
    sessions: List[PresetSessionCreate]

class PresetPomodoroOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    sessions: List[PresetSessionOut]

    model_config = {"from_attributes": True}
