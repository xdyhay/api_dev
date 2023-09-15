"""add user fkey column to posts

Revision ID: 0afa0bf2b3c8
Revises: dbb482cbce41
Create Date: 2023-09-14 17:42:22.239852

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0afa0bf2b3c8'
down_revision: Union[str, None] = 'dbb482cbce41'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('user_uuid', sa.UUID(as_uuid=True), nullable=False),
    )
    op.create_foreign_key(
        'posts_user_uuid_fkey',
        source_table='posts', 
        referent_table='users', 
        local_cols=['user_uuid'], 
        remote_cols=['uuid'], 
        ondelete='CASCADE'
    )


def downgrade() -> None:
    op.drop_column('posts', 'user_uuid')
    op.drop_constraint('posts_user_uuid_fkey', 'posts', type_='foreignkey')
