"""add user table

Revision ID: 58a837f852f8
Revises: ad69c798dee9
Create Date: 2023-09-13 00:17:15.903426

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '58a837f852f8'
down_revision: Union[str, None] = 'ad69c798dee9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'test_users',
        sa.Column('uuid', sa.UUID(as_uuid=True), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), 
                  server_default=sa.text('current_timestamp'), nullable=False),
        sa.PrimaryKeyConstraint('uuid'),
        sa.UniqueConstraint('email')
    )


def downgrade() -> None:
    op.drop_table('test_users')
