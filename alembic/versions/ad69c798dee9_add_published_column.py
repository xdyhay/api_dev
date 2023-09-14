"""add published column

Revision ID: ad69c798dee9
Revises: 6f0960effe15
Create Date: 2023-09-13 00:06:17.383075

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ad69c798dee9'
down_revision: Union[str, None] = '6f0960effe15'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('test_posts', sa.Column('published', sa.Boolean(), nullable=False))


def downgrade() -> None:
    op.drop_column('test_posts', 'published')
