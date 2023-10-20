"""create post table

Revision ID: fac34fdcf9f8
Revises: 
Create Date: 2023-10-19 18:07:48.305792

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fac34fdcf9f8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),sa.Column('title', sa.String(), nullable=False)) 
    pass


def downgrade() -> None:
    op.drop_table('posts') 

    pass
