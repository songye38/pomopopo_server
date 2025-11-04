# sqlalchemy 모델 정의
# 이 파일은 데이터베이스 테이블 구조를 정의합니다.

from sqlalchemy import Table, Column, Integer, String,ForeignKey,DateTime,Boolean,UUID,Enum,event,text
from sqlalchemy.orm import relationship
from app.db.database import Base,engine
from sqlalchemy.orm import Session as ORMSession  # ⚠️ 여기 주의
import app.db.models as models
from datetime import datetime
import uuid
import enum



class SessionStatus(str, enum.Enum):
    NOT_STARTED = "not_started"   # 아직 시작하지 않음
    ABORTED = "aborted"           # 중간에 그만둠
    COMPLETED = "completed"       # 완료함

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
    stats = relationship("UserStats", uselist=False, back_populates="user")


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
    session_type = relationship("SessionType", back_populates="sessions")
    pomodoro = relationship("Pomodoro", back_populates="sessions")
    session_logs = relationship("SessionLog", back_populates="session")


# --------------------------
# UserPomodoroLog
# --------------------------
class UserPomodoroLog(Base):
    __tablename__ = "user_pomodoro_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    pomodoro_id = Column(UUID(as_uuid=True), ForeignKey("pomodoros.id"),nullable=False)

    started_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime, nullable=True)
    total_effective_duration = Column(Integer, default=0, nullable=False) #실제 집중한 시간 -> 세션들의 실제 집중시간 합을 더해 구한다. 
    completed = Column(Boolean, default=False)
    status = Column(Enum(SessionStatus), default=SessionStatus.NOT_STARTED, nullable=False)
    

    comment = Column(String, nullable=True)
    rating = Column(Integer, nullable=True)

    # 관계
    user = relationship("User", back_populates="pomodoro_logs")
    pomodoro = relationship("Pomodoro", back_populates="logs")
    sessions = relationship("SessionLog", back_populates="log")

    @property
    def average_focus_rate(self):
        """전체 세션들의 평균 집중률"""
        if not self.sessions:
            return 0
        return round(
            sum(s.focus_rate for s in self.sessions if s.planned_duration) / len(self.sessions),
            1,
        )


# --------------------------
# SessionLog
# --------------------------
class SessionLog(Base):
    __tablename__ = "session_logs"

    id = Column(Integer, primary_key=True, index=True)
    log_id = Column(UUID(as_uuid=True), ForeignKey("user_pomodoro_logs.id"), nullable=False)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)

    goal = Column(String, nullable=False)
    order = Column(Integer)
    completed = Column(Boolean, default=False) #ui 표시를 위해 그대로 놔두기 
    status = Column(Enum(SessionStatus), default=SessionStatus.NOT_STARTED, nullable=False)

    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)

    # ⏱ 시간 관련 필드
    planned_duration = Column(Integer, nullable=False)  # 사용자가 정한 목표 시간
    actual_duration = Column(Integer, default=0, nullable=False)  # 타이머가 실제로 돈 시간 (일시정지 포함)
    total_paused_duration = Column(Integer, default=0, nullable=False)
    effective_duration = Column(Integer, default=0, nullable=False)  # 실제 집중 시간
    missed_duration = Column(Integer, default=0, nullable=False)  # 계획 대비 빠진 시간


    # 관계
    log = relationship("UserPomodoroLog", back_populates="sessions")
    session = relationship("Session", back_populates="session_logs")

    # ✅ 실제 집중 시간 계산 속성
    def recalculate_durations(self):
        """모든 duration 관련 필드를 일관성 있게 재계산"""
        if self.started_at and self.finished_at:
            self.actual_duration = int((self.finished_at - self.started_at).total_seconds())
        else:
            self.actual_duration = 0

        self.effective_duration = max(
            self.actual_duration - (self.total_paused_duration or 0), 0
        )
        self.missed_duration = max(
            (self.planned_duration or 0) - self.effective_duration, 0
        )

    @property
    def focus_rate(self):
        """계획 대비 실제 집중 비율 (0~100%)"""
        if not self.planned_duration:
            return 0
        return round((self.effective_duration / self.planned_duration) * 100, 1)
    


class UserStats(Base):
    __tablename__ = "user_stats"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    total_pomodoros = Column(Integer, default=0)  # 총 뽀모도로 실행 횟수
    total_sessions = Column(Integer, default=0)  # 총 세션 수
    total_focus_duration = Column(Integer, default=0)  # 누적 집중 시간 (초 단위)
    average_focus_rate = Column(Integer, default=0)  # 평균 집중률 (0~100)
    last_active_at = Column(DateTime, nullable=True)  # 마지막 활동 시각

    user = relationship("User", back_populates="stats")



# ✅ SQLAlchemy 세션 이벤트 훅 등록
@event.listens_for(ORMSession, "before_flush")
def auto_recalculate_durations(session, flush_context, instances):
    updated_logs = set()

    for obj in session.dirty:
        if isinstance(obj, SessionLog):
            obj.recalculate_durations()
            updated_logs.add(obj.log)  # 변경된 세션로그의 상위 로그 기록

    # 상위 로그 합산 처리
    for log in updated_logs:
        if log.sessions:
            log.total_effective_duration = sum(s.effective_duration for s in log.sessions)

@event.listens_for(SessionLog, "before_update")
def sync_completed_flag(mapper, connection, target):
    target.completed = target.status == SessionStatus.COMPLETED




# 뽀모도로 완료시 사용자의 stats 테이블을 수정함 
@event.listens_for(UserPomodoroLog, "after_update")
def update_user_stats_on_finish(mapper, connection, target):
    """뽀모도로 로그 완료 시 유저 통계 갱신 및 자동 생성"""
    # ✅ 상태가 COMPLETED인지 확인 (Enum 혹은 문자열 둘 다 처리)
    if str(target.status) not in [SessionStatus.COMPLETED, "completed"]:
        return

    user_id = str(target.user_id)
    total_focus = target.total_effective_duration or 0
    finished_at = target.finished_at or datetime.utcnow()
    new_focus_rate = target.average_focus_rate or 0  # 새로 완료된 세션의 평균 집중률

    # ✅ 통계 자동 생성 및 업데이트 (upsert)
    connection.execute(
        text("""
        INSERT INTO user_stats (
            user_id, total_pomodoros, total_sessions,
            total_focus_duration, average_focus_rate, last_active_at
        )
        VALUES (:user_id, 1, 0, :focus, :focus_rate, :finished)
        ON CONFLICT (user_id)
        DO UPDATE SET
            total_pomodoros = user_stats.total_pomodoros + 1,
            total_focus_duration = user_stats.total_focus_duration + :focus,
            average_focus_rate = ROUND(
                ((user_stats.average_focus_rate * user_stats.total_pomodoros) + :focus_rate)
                / (user_stats.total_pomodoros + 1)
            ),
            last_active_at = :finished
        """),
        {
            "user_id": user_id,
            "focus": total_focus,
            "focus_rate": new_focus_rate,
            "finished": finished_at,
        },
    )
