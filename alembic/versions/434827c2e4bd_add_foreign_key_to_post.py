"""add foreign key to post

Revision ID: 434827c2e4bd
Revises: 58a837f852f8
Create Date: 2023-09-13 00:33:56.143668

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '434827c2e4bd'
down_revision: Union[str, None] = '58a837f852f8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('test_posts', sa.Column('user_uuid', sa.UUID(as_uuid=True), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='test_posts', referent_table='test_users', local_cols=['user_uuid'], remote_cols=['uuid'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='test_posts', type_='foreignkey')
    op.drop_column('test_posts', 'user_uuid')
