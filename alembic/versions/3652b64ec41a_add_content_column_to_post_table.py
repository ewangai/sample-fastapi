"""add content column to post table

Revision ID: 3652b64ec41a
Revises: fac34fdcf9f8
Create Date: 2023-10-19 18:17:03.783697

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3652b64ec41a'
down_revision: Union[str, None] = 'fac34fdcf9f8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
