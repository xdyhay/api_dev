"""add content column

Revision ID: 6f0960effe15
Revises: 622875cdef0b
Create Date: 2023-09-12 23:57:40.515593

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6f0960effe15'
down_revision: Union[str, None] = '622875cdef0b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('test_posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('test_posts', 'content')
