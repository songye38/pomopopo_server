# sqlalchemy 모델 정의
# 이 파일은 데이터베이스 테이블 구조를 정의합니다.

from sqlalchemy import Column, Integer, String,ForeignKey,DateTime,Boolean,UUID
from sqlalchemy.orm import relationship
from app.db.database import Base,engine
import app.db.models as models
from datetime import datetime
import uuid


# User 모델 정의
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    name = Column(String)  # ✅ DB에 꼭 저장됨

    # User가 만든 Pomodoro 리스트
    pomodoros = relationship("Pomodoro", back_populates="user")



# 세션 타입 정의 
class SessionType(Base):
    __tablename__ = "session_types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)

    # ORM에서 Session 연결
    sessions = relationship("Session", back_populates="session_type")


class Pomodoro(Base):
    __tablename__ = "pomodoros"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))  # 사용자 연결
    sessions = relationship("Session", back_populates="pomodoro")

    # ORM에서 User와 연결
    user = relationship("User", back_populates="pomodoros")


#세션 테이블
class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, index=True)
    pomodoro_id = Column(Integer, ForeignKey("pomodoros.id"))
    type_id = Column(Integer, ForeignKey("session_types.id"))
    goal = Column(String, nullable=False)
    duration = Column(Integer)
    order = Column(Integer)
    
    pomodoro = relationship("Pomodoro", back_populates="sessions")
    session_type = relationship("SessionType", back_populates="sessions")




# 프리셋 뽀모도로
class PresetPomodoro(Base):
    __tablename__ = "preset_pomodoros"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    sessions = relationship("PresetSession", back_populates="preset")


#프리셋 뽀모도로에 사용될 세션
class PresetSession(Base):
    __tablename__ = "preset_sessions"
    id = Column(Integer, primary_key=True, index=True)
    preset_id = Column(Integer, ForeignKey("preset_pomodoros.id"))
    type_id = Column(Integer, ForeignKey("session_types.id"))
    goal = Column(String, nullable=False)
    duration = Column(Integer)
    order = Column(Integer)

    preset = relationship("PresetPomodoro", back_populates="sessions")
    session_type = relationship("SessionType")


class UserPomodoroLog(Base):
    __tablename__ = "user_pomodoro_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    pomodoro_id = Column(Integer, ForeignKey("pomodoros.id"))
    started_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime, nullable=True)
    total_duration = Column(Integer, nullable=True)
    completed = Column(Boolean, default=False)

    user = relationship("User")
    pomodoro = relationship("Pomodoro")
    sessions = relationship("SessionLog", back_populates="log")

class SessionLog(Base):
    __tablename__ = "session_logs"
    id = Column(Integer, primary_key=True, index=True)
    log_id = Column(Integer, ForeignKey("user_pomodoro_logs.id"))
    session_id = Column(Integer, ForeignKey("sessions.id"))
    goal = Column(String, nullable=False)
    duration = Column(Integer)
    order = Column(Integer)
    completed = Column(Boolean, default=False)

    log = relationship("UserPomodoroLog", back_populates="sessions")
    session = relationship("Session")