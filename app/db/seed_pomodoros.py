from app.db.database import SessionLocal
from app.db.models import Pomodoro, Session
import uuid
from datetime import datetime

db = SessionLocal()

def seed_pomodoros():
    """기본 프리셋 뽀모도로 및 세션 데이터 삽입"""
    try:
        # ✅ 기본 뽀모도로들
        default_pomodoros = [
            {
                "title": "refine",
                "sessions": [
                    { "order": 1, "duration": 25, "goal": "생각나는 아이디어를 제한 없이 쭉 적어보기" ,"type_id":1,"name":'발산'},
                    { "order": 2, "duration": 5, "goal": "머리를 비우고 잠깐 쉬기","type_id":14 ,"name":'단기휴식'},
                    { "order": 3, "duration": 25, "goal": "주변 현상이나 대상을 주의 깊게 보고 기록하기","type_id":3 ,"name":'관찰'},
                    { "order": 4, "duration": 5, "goal": "머리를 비우고 잠깐 쉬기","type_id":14,"name":'단기휴식' },
                    { "order": 5, "duration": 25, "goal": "결과","type_id":4 ,"name":'스크리닝'},
                    { "order": 6, "duration": 25, "goal": "머릿속 생각을 자유롭게 흘려보내고, 최소한의 행동/표현으로 감각 유지","type_id":15,"name":'장기휴식' },
                ],
            },
            {
                "title": "reverse",
                "sessions": [
                    { "order": 1, "duration": 25,"goal": "발산한 아이디어 중 중요한 것만 골라 구체화하기", "type_id":2 ,"name":'수렴'},
                    { "order": 2, "duration": 5,"goal": "머리를 비우고 잠깐 쉬기", "type_id": 14,"name":'단기휴식' },
                    { "order": 3, "duration": 5,"goal": "주변 현상이나 대상을 주의 깊게 보고 기록하기", "type_id":3 ,"name":'관찰'},
                    { "order": 4, "duration": 5,"goal": "머리를 비우고 잠깐 쉬기", "type_id":14,"name":'단기휴식' },
                    { "order": 5, "duration": 25,"goal": "기존 아이디어를 뒤집어 새 관점으로 재배치하기", "type_id": 6 ,"name":'뒤집기 사고'},
                    { "order": 6, "duration": 25,"goal": "머릿속 생각을 자유롭게 흘려보내고, 최소한의 행동/표현으로 감각 유지", "type_id": 15 ,"name":'장기휴식'},
                ],
            },
            {
                "title": "random",
                "sessions": [
                   { "order": 1, "duration": 25,"goal": "생각나는 아이디어를 제한 없이 쭉 적어보기", "type_id": 1 ,"name":'발산'},
                    { "order": 2, "duration": 5,"goal": "머리를 비우고 잠깐 쉬기", "type_id": 14,"name":'단기휴식' },
                    { "order": 3, "duration": 25,"goal": "무작위 아이디어에 현실적인 규칙 적용해 보기", "type_id": 7 ,"name":'제약 도입'},
                    { "order": 4, "duration": 5, "goal": "머리를 비우고 잠깐 쉬기", "type_id": 14,"name":'단기휴식' },
                    { "order": 5,"duration": 25,"goal": "생각나는 아이디어를 제한 없이 쭉 적어보기", "type_id":1 ,"name":'발산'},
                    { "order": 6,"duration": 25,"goal": "머릿속 생각을 자유롭게 흘려보내고, 최소한의 행동/표현으로 감각 유지", "type_id": 15,"name":'장기휴식' },
                ],
            },
            {
                "title": "emotion",
                "sessions": [
                    { "order": 1, "duration": 25,"goal": "생각나는 아이디어를 제한 없이 쭉 적어보기", "type_id": 1,"name":'발산' },
                    { "order": 2, "duration": 5,"goal": "머리를 비우고 잠깐 쉬기", "type_id": 14,"name":'단기휴식' },
                    { "order": 3, "duration": 25,"goal": "지금 느끼는 감정을 글이나 그림으로 기록하기", "type_id": 8,"name":'감정 기록' },
                    { "order": 4, "duration": 5, "goal": "머리를 비우고 잠깐 쉬기", "type_id": 14 ,"name":'단기휴식'},
                    { "order": 5, "duration": 25,"goal": "생각나는 아이디어를 제한 없이 쭉 적어보기", "type_id": 1,"name":'발산' },
                    { "order": 6, "duration": 25, "goal": "머릿속 생각을 자유롭게 흘려보내고, 최소한의 행동/표현으로 감각 유지", "type_id": 15,"name":'장기휴식' },
                ],
            },
            {
                "title": "explore",
                "sessions": [
                    { "order": 1, "duration": 25,"goal": "생각나는 아이디어를 제한 없이 쭉 적어보기", "type_id":1,"name":'발산' },
                    { "order": 2, "duration": 5,"goal": "머리를 비우고 잠깐 쉬기", "type_id": 14,"name":'단기휴식' },
                    { "order": 3, "duration": 25,"goal": "아이디어에 키워드나 카테고리를 붙여 정리하기", "type_id": 9 ,"name":'아이디어 태깅'},
                    { "order": 4, "duration": 5,"goal": "머리를 비우고 잠깐 쉬기", "type_id": 14,"name":'단기휴식' },
                    { "order": 5, "duration": 25,"goal": "생각나는 아이디어를 제한 없이 쭉 적어보기", "type_id": 1,"name":'발산' },
                    { "order": 6, "duration": 25, "goal": "머릿속 생각을 자유롭게 흘려보내고, 최소한의 행동/표현으로 감각 유지", "type_id": 15,"name":'장기휴식' },
                ],
            },
            {
                "title": "story",
                "sessions": [
                    { "order": 1, "duration": 25,"goal": "발산한 아이디어 중 중요한 것만 골라 구체화하기", "type_id": 2 ,"name":'수렴'},
                    { "order": 2, "duration": 5,"goal": "머리를 비우고 잠깐 쉬기", "type_id": 14,"name":'단기휴식' },
                    { "order": 3, "duration": 25, "goal": "전체 흐름을 단계별로 설계하고 연결 확인하기", "type_id": 10,"name":'구조화' },
                    { "order": 4, "duration": 5,  "goal": "머리를 비우고 잠깐 쉬기", "type_id": 14 ,"name":'단기휴식'},
                    { "order": 5, "duration": 25, "goal": "발산한 아이디어 중 중요한 것만 골라 구체화하기", "type_id": 2,"name":'수렴' },
                    { "order": 6, "duration": 25, "goal": "머릿속 생각을 자유롭게 흘려보내고, 최소한의 행동/표현으로 감각 유지", "type_id": 15,"name":'장기휴식' },
                ],
            },
            {
                "title": "echo",
                "sessions": [
                    { "order": 1, "duration": 25, "goal": "주변 현상이나 대상을 주의 깊게 보고 기록하기", "type_id": 3,"name":'관찰' },
                    { "order": 2, "duration": 5, "goal": "머리를 비우고 잠깐 쉬기", "type_id":14,"name":'단기휴식' },
                    { "order": 3, "duration": 25, "goal": "작업 중 느낀 감정을 기록하고 패턴 확인하기", "type_id": 11,"name":'반응 분석'},
                    { "order": 4, "duration": 5, "goal": "머리를 비우고 잠깐 쉬기", "type_id": 14,"name":'단기휴식' },
                    { "order": 5, "duration": 25, "goal": "주변 현상이나 대상을 주의 깊게 보고 기록하기", "type_id": 3 ,"name":'관찰'},
                    { "order": 6, "duration": 25, "goal": "머릿속 생각을 자유롭게 흘려보내고, 최소한의 행동/표현으로 감각 유지", "type_id": 15,"name":'장기휴식' },
                ],
            },
            {
                "title": "escape",
                "sessions": [
                    { "order": 1, "duration": 25, "goal": "생각나는 아이디어를 제한 없이 쭉 적어보기", "type_id":1,"name":'발산' },
                    { "order": 2, "duration": 5, "goal": "머리를 비우고 잠깐 쉬기", "type_id": 14 ,"name":'단기휴식'},
                    { "order": 3,"duration": 25, "goal": "기존 규칙을 과감히 벗어나 새 방식 시도하기", "type_id": 12,"name":'규칙 탈착' },
                    { "order": 4, "duration": 5, "goal": "머리를 비우고 잠깐 쉬기", "type_id": 14,"name":'단기휴식' },
                    { "order": 5, "duration": 25, "goal": "생각나는 아이디어를 제한 없이 쭉 적어보기", "type_id":1,"name":'발산' },
                    { "order": 6, "duration": 25, "goal": "머릿속 생각을 자유롭게 흘려보내고, 최소한의 행동/표현으로 감각 유지", "type_id": 15,"name":'장기휴식' },
                ],
            },
            {
                "title": "repeat",
                "sessions": [
                    { "order": 1,"duration": 25, "goal": "생각나는 아이디어를 제한 없이 쭉 적어보기", "type_id":1,"name":'발산' },
                    { "order": 2, "duration": 5, "goal": "머리를 비우고 잠깐 쉬기", "type_id": 14 ,"name":'단기휴식'},
                    { "order": 3, "duration": 25, "goal": "발산한 아이디어 중 중요한 것만 골라 구체화하기", "type_id": 2,"name":'수렴' },
                    { "order": 4, "duration": 5,"goal": "머리를 비우고 잠깐 쉬기", "type_id": 14,"name":'단기휴식' },
                    { "order": 5, "duration": 25, "goal": "아이디어를 여러 방식으로 변형하며 발전시키기", "type_id": 13,"name":'변형' },
                    { "order": 6, "duration": 25, "goal": "머릿속 생각을 자유롭게 흘려보내고, 최소한의 행동/표현으로 감각 유지", "type_id": 15,"name":'장기휴식' },
                ],
            },
            {
                "title": "empty",
                "sessions": [
                    { "order": 1, "duration": 25, "goal": "생각나는 아이디어를 제한 없이 쭉 적어보기", "type_id":1,"name":'발산' },
                    { "order": 2, "duration": 5, "goal": "머리를 비우고 잠깐 쉬기", "type_id": 14,"name":'단기휴식' },
                    { "order": 3, "duration": 5, "goal": "주변 현상이나 대상을 주의 깊게 보고 기록하기", "type_id": 3,"name":'관찰' },
                    { "order": 4, "duration": 5, "goal": "머리를 비우고 잠깐 쉬기", "type_id": 14 ,"name":'단기휴식'},
                    { "order": 5, "duration": 25, "goal": "생각나는 아이디어를 제한 없이 쭉 적어보기", "type_id":1,"name":'발산' },
                    { "order": 6, "duration": 25, "goal": "머릿속 생각을 자유롭게 흘려보내고, 최소한의 행동/표현으로 감각 유지", "type_id": 15,"name":'장기휴식' },
                ],
            }
        ]

        for p in default_pomodoros:
            # 중복 체크 (title 기준)
            existing = db.query(Pomodoro).filter_by(title=p["title"]).first()
            if existing:
                continue

            pomodoro = Pomodoro(
                id=uuid.uuid4(),
                title=p["title"],
                user_id=None,  # 프리셋은 null
            )
            db.add(pomodoro)
            db.commit()
            db.refresh(pomodoro)

            # 하위 세션 추가
            for s in p["sessions"]:
                session = Session(
                    pomodoro_id=pomodoro.id,
                    goal=s["goal"],
                    duration=s["duration"],
                    order=s["order"],
                    name=s["name"],
                    type_id=s["type_id"], 
                )
                db.add(session)

            db.commit()

        print("✅ 기본 프리셋 뽀모도로 및 세션 데이터 삽입 완료!")

    except Exception as e:
        db.rollback()
        print(f"🚨 오류 발생: {e}")

    finally:
        db.close()
