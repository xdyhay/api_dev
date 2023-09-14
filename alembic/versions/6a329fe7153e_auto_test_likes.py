"""auto-test_likes

Revision ID: 6a329fe7153e
Revises: 434827c2e4bd
Create Date: 2023-09-13 23:35:44.373891

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '6a329fe7153e'
down_revision: Union[str, None] = '434827c2e4bd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('test_likes', 
                    sa.Column('post.id', sa.Integer(), nullable=False), 
                    sa.Column('user.uuid', sa.UUID(), nullable=False), 
                    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False), 
                    sa.ForeignKeyConstraint(['post.id'], ['test_posts.id'], name='like_posts_fk', ondelete='CASCADE'), 
                    sa.ForeignKeyConstraint(['user.uuid'], ['test_users.uuid'], name='like_users_fk', ondelete='CASCADE'), 
                    sa.PrimaryKeyConstraint('post.id', 'user.uuid', name='test_likes_pkey'))


def downgrade() -> None:
    op.drop_table('test_likes')
