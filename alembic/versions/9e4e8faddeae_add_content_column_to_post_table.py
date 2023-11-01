"""add content column to post table

Revision ID: 9e4e8faddeae
Revises: 8bf387510c3a
Create Date: 2023-11-01 13:52:11.912986

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9e4e8faddeae'
down_revision: Union[str, None] = '8bf387510c3a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
