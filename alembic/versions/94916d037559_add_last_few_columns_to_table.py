"""add last few columns to table

Revision ID: 94916d037559
Revises: 8e1c8602ec34
Create Date: 2023-10-20 12:44:28.698925

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '94916d037559'
down_revision: Union[str, None] = '8e1c8602ec34'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade(): # -> None:
    op.drop_column('posts', 'published')
    op.drop_column('created_at', 'published')
    pass
