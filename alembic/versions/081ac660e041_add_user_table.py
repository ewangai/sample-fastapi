"""add user table

Revision ID: 081ac660e041
Revises: 3652b64ec41a
Create Date: 2023-10-19 18:28:02.660084

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '081ac660e041'
down_revision: Union[str, None] = '3652b64ec41a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('users', 
                  sa.Column('id', sa.Integer(), nullable=False),
                  sa.Column('email', sa.String(), nullable=False),
                  sa.Column('password', sa.String(), nullable=False),
                  sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                            server_default=sa.text('now()'), nullable=False),
                  sa.PrimaryKeyConstraint('id'),
                  sa.UniqueConstraint('email')
                  )
    pass


def downgrade():
    op.drop_table('users')
    pass

