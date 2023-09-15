"""create users table

Revision ID: dbb482cbce41
Revises: 795dbb3874e2
Create Date: 2023-09-14 17:39:37.803980

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dbb482cbce41'
down_revision: Union[str, None] = '795dbb3874e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('uuid', sa.UUID(as_uuid=True), index=True, nullable=False, server_default=sa.text('gen_random_uuid()'), unique=True),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), 
                  server_default=sa.text('current_timestamp'), nullable=False),
        sa.PrimaryKeyConstraint('uuid'),
        sa.UniqueConstraint('email')
    )


def downgrade() -> None:
    op.drop_table('users')
