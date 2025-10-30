# sqlalchemy 모델 정의
# 이 파일은 데이터베이스 테이블 구조를 정의합니다.

from sqlalchemy import Table, Column, Integer, String,ForeignKey,DateTime,Boolean,UUID
from sqlalchemy.orm import relationship
from app.db.database import Base,engine
import app.db.models as models
from datetime import datetime
import uuid




# 세션 타입 정의 
class SessionType(Base):
    __tablename__ = "session_types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)

    # ORM에서 Session 연결
    sessions = relationship("Session", back_populates="session_type")


# --------------------------
# User
# --------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    name = Column(String)

    # 관계
    pomodoros = relationship("Pomodoro", back_populates="user")
    pomodoro_logs = relationship("UserPomodoroLog", back_populates="user")


# --------------------------
# Pomodoro
# --------------------------
class Pomodoro(Base):
    __tablename__ = "pomodoros"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)  # 프리셋은 null 가능

    # 관계
    user = relationship("User", back_populates="pomodoros")
    sessions = relationship("Session", back_populates="pomodoro")
    logs = relationship("UserPomodoroLog", back_populates="pomodoro")


# --------------------------
# Session
# --------------------------
class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    pomodoro_id = Column(UUID(as_uuid=True), ForeignKey("pomodoros.id"))
    type_id = Column(Integer, ForeignKey("session_types.id"))
    goal = Column(String, nullable=False)
    duration = Column(Integer)
    order = Column(Integer)
    name = Column(String, nullable=True)

    # 관계
    pomodoro = relationship("Pomodoro", back_populates="sessions")
    session_logs = relationship("SessionLog", back_populates="session")


# --------------------------
# UserPomodoroLog
# --------------------------
class UserPomodoroLog(Base):
    __tablename__ = "user_pomodoro_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    pomodoro_id = Column(UUID(as_uuid=True), ForeignKey("pomodoros.id"))

    started_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime, nullable=True)
    total_duration = Column(Integer, nullable=True)
    completed = Column(Boolean, default=False)

    comment = Column(String, nullable=True)
    rating = Column(Integer, nullable=True)

    # 관계
    user = relationship("User", back_populates="pomodoro_logs")
    pomodoro = relationship("Pomodoro", back_populates="logs")
    sessions = relationship("SessionLog", back_populates="log")


# --------------------------
# SessionLog
# --------------------------
class SessionLog(Base):
    __tablename__ = "session_logs"

    id = Column(Integer, primary_key=True, index=True)
    log_id = Column(UUID(as_uuid=True), ForeignKey("user_pomodoro_logs.id"), nullable=False)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=True)

    goal = Column(String, nullable=False)
    duration = Column(Integer)
    order = Column(Integer)
    completed = Column(Boolean, default=False)

    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)

    pause_count = Column(Integer, default=0)           # 몇 번 일시정지 했는지
    total_paused_duration = Column(Integer, default=0) # 총 일시정지 시간(초)

    # 관계
    log = relationship("UserPomodoroLog", back_populates="sessions")
    session = relationship("Session", back_populates="session_logs")
