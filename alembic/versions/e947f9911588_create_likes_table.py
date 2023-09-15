"""create likes table

Revision ID: e947f9911588
Revises: 0afa0bf2b3c8
Create Date: 2023-09-14 17:53:18.705230

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e947f9911588'
down_revision: Union[str, None] = '0afa0bf2b3c8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'likes', 
        sa.Column('post_id', sa.Integer(), nullable=False), 
        sa.Column('user_uuid', sa.UUID(), nullable=False), 
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False), 
        sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'), 
        sa.ForeignKeyConstraint(['user_uuid'], ['users.uuid'], ondelete='CASCADE'), 
        sa.PrimaryKeyConstraint('post_id', 'user_uuid')
    )


def downgrade() -> None:
    op.drop_table('likes')
