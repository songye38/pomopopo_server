
# 이 파일은 사용자 인증과 관련된 CRUD 작업을 수행하는 모듈입니다.
# 사용자 생성, 조회, 비밀번호 해시화 및 검증 기능을 포함합니다.
# 이 모듈은 FastAPI와 SQLAlchemy를 사용하여 데이터베이스와 상호작용합니다.


from sqlalchemy.orm import Session
from app.db.models import User
from passlib.context import CryptContext
from app.db import models
from app.db.models import User, UserStats

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 비밀번호 해시 함수
def get_password_hash(password: str):
    return pwd_context.hash(password)


# 구 버전 사용자 생성 함수
# def create_user(db: Session, email: str, password: str | None, name: str):
#     if password is not None:
#         hashed_pw = get_password_hash(password)
#     else:
#         hashed_pw = None

#     db_user = User(email=email, hashed_password=hashed_pw, name=name)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user




# -----------------------------------------
# 사용자 생성하면서 유저 통계 정보도 함께 기본으로 세팅
# -----------------------------------------
def create_user(db: Session, email: str, password: str | None, name: str):
    # ✅ 비밀번호 해싱
    hashed_pw = get_password_hash(password) if password else None

    # ✅ 유저 생성
    db_user = User(email=email, hashed_password=hashed_pw, name=name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # ✅ 유저 통계 기본값 세팅
    user_stats = UserStats(
        user_id=db_user.id,
        total_pomodoros=0,
        total_sessions=0,
        total_focus_duration=0,
        average_focus_rate=0,
        last_active_at=None
    )
    db.add(user_stats)
    db.commit()

    # ✅ 완성된 유저 반환
    db.refresh(db_user)
    return db_user



# 사용자 조회 함수 추가
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


# 비밀번호 검증 함수
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)