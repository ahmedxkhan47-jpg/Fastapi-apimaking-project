"""add content column to posts table

Revision ID: 9797b689ef35
Revises: 9313b3f2dba6
Create Date: 2026-06-27 05:18:58.284336

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9797b689ef35'
down_revision: Union[str, Sequence[str], None] = '9313b3f2dba6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
