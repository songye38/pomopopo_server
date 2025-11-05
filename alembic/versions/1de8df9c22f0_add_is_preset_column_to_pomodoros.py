"""add is_preset column to pomodoros

Revision ID: 1de8df9c22f0
Revises: d5137798e470
Create Date: 2025-11-05 16:12:46.926252
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '1de8df9c22f0'
down_revision: Union[str, Sequence[str], None] = 'd5137798e470'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1️⃣ 컬럼 추가 (처음엔 nullable=True 로 추가해야 기존 데이터에 영향 없음)
    op.add_column('pomodoros', sa.Column('is_preset', sa.Boolean(), nullable=True))

    # 2️⃣ 기존 데이터 기준으로 값 채우기
    # user_id 가 NULL → 프리셋(True)
    # user_id 있는 데이터 → 일반(False)
    op.execute("UPDATE pomodoros SET is_preset = TRUE WHERE user_id IS NULL;")
    op.execute("UPDATE pomodoros SET is_preset = FALSE WHERE user_id IS NOT NULL;")

    # 3️⃣ null 금지 + default 값 설정
    op.alter_column(
        'pomodoros',
        'is_preset',
        existing_type=sa.Boolean(),
        nullable=False,
        server_default=sa.text('FALSE')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('pomodoros', 'is_preset')
