# sqlalchemy 모델 정의
# 이 파일은 데이터베이스 테이블 구조를 정의합니다.

from sqlalchemy import Table, Column, Integer, String,ForeignKey,DateTime,Boolean,UUID,CheckConstraint
from sqlalchemy.orm import relationship
from app.db.database import Base,engine
import app.db.models as models
from datetime import datetime
import uuid

# User 모델 정의
class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    name = Column(String)  # ✅ DB에 꼭 저장됨

    # User가 만든 Pomodoro 리스트
    pomodoros = relationship("Pomodoro", back_populates="user")
    pomodoro_logs = relationship("UserPomodoroLog", back_populates="user")



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
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))  # UUID로 변경
    sessions = relationship("Session", back_populates="pomodoro")

    # ORM에서 User와 연결
    user = relationship("User", back_populates="pomodoros")
    logs = relationship("UserPomodoroLog", back_populates="pomodoro")


#세션 테이블
class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, index=True)
    pomodoro_id = Column(UUID(as_uuid=True), ForeignKey("pomodoros.id"))
    type_id = Column(Integer, ForeignKey("session_types.id"))
    goal = Column(String, nullable=False)
    duration = Column(Integer)
    order = Column(Integer)
    name = Column(String, nullable=True)

    pomodoro = relationship("Pomodoro", back_populates="sessions")
    session_type = relationship("SessionType", back_populates="sessions")
    session_logs = relationship("SessionLog", back_populates="session")



# 중간 테이블을 Association Object로 정의
class PresetPomodoroSession(Base):
    __tablename__ = "preset_pomodoro_sessions"
    id = Column(Integer, primary_key=True, index=True)  # 🔹 새로 추가
    preset_id = Column(Integer, ForeignKey("preset_pomodoros.id"))
    session_id = Column(Integer, ForeignKey("preset_sessions.id"))
    order = Column(Integer)

    preset = relationship("PresetPomodoro", back_populates="preset_sessions")
    session = relationship("PresetSession")

# 프리셋 뽀모도로
class PresetPomodoro(Base):
    __tablename__ = "preset_pomodoros"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)

    preset_sessions = relationship(
        "PresetPomodoroSession",
        back_populates="preset",
        order_by="PresetPomodoroSession.order"
    )

    @property
    def sessions(self):
        # order 기준으로 세션 리스트 반환
        return [ps.session for ps in self.preset_sessions]

    logs = relationship("UserPomodoroLog", back_populates="preset_pomodoro")


class PresetSession(Base):
    __tablename__ = "preset_sessions"
    id = Column(Integer, primary_key=True, index=True)
    type_id = Column(Integer, ForeignKey("session_types.id"))
    goal = Column(String, nullable=False)
    duration = Column(Integer)
    name = Column(String, nullable=True)

    session_type = relationship("SessionType")
    presets = relationship(
        "PresetPomodoroSession",
        back_populates="session"
    )

    session_logs = relationship("SessionLog", back_populates="preset_session")


class UserPomodoroLog(Base):
    __tablename__ = "user_pomodoro_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # 두 가지 중 하나만 채워짐
    pomodoro_id = Column(UUID(as_uuid=True), ForeignKey("pomodoros.id"), nullable=True)
    preset_pomodoro_id = Column(Integer, ForeignKey("preset_pomodoros.id"), nullable=True)

    started_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime, nullable=True)
    total_duration = Column(Integer, nullable=True)
    completed = Column(Boolean, default=False)


    comment = Column(String, nullable=True)
    rating = Column(Integer, nullable=True)

    # 관계 설정
    user = relationship("User", back_populates="pomodoro_logs")
    pomodoro = relationship("Pomodoro", back_populates="logs")
    preset_pomodoro = relationship("PresetPomodoro", back_populates="logs")

    sessions = relationship("SessionLog", back_populates="log")

    # 둘 중 하나만 존재해야 함
    __table_args__ = (
        CheckConstraint(
            "(pomodoro_id IS NOT NULL AND preset_pomodoro_id IS NULL) OR "
            "(pomodoro_id IS NULL AND preset_pomodoro_id IS NOT NULL)",
            name="only_one_pomodoro_type"
        ),
    )

class SessionLog(Base):
    __tablename__ = "session_logs"

    id = Column(Integer, primary_key=True, index=True)
    log_id = Column(UUID(as_uuid=True), ForeignKey("user_pomodoro_logs.id"), nullable=False)

    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=True)
    preset_session_id = Column(Integer, ForeignKey("preset_sessions.id"), nullable=True)

    goal = Column(String, nullable=False)
    duration = Column(Integer)
    order = Column(Integer)
    completed = Column(Boolean, default=False)

    # ✅ 추가
    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)

    pause_count = Column(Integer, default=0)          # 몇 번 일시정지 했는지
    total_paused_duration = Column(Integer, default=0) # 총 일시정지 시간(초)

    log = relationship("UserPomodoroLog", back_populates="sessions")
    session = relationship("Session", back_populates="session_logs")
    preset_session = relationship("PresetSession", back_populates="session_logs")

    __table_args__ = (
        CheckConstraint(
            "(session_id IS NOT NULL AND preset_session_id IS NULL) OR "
            "(session_id IS NULL AND preset_session_id IS NOT NULL)",
            name="only_one_session_type"
        ),
    )
