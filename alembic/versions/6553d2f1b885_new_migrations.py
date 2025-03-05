"""new_migrations

Revision ID: 6553d2f1b885
Revises: 13fc969cbd7f
Create Date: 2025-03-04 22:16:01.929773

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6553d2f1b885'
down_revision: Union[str, None] = '13fc969cbd7f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'authors', ['full_name'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'authors', type_='unique')
    # ### end Alembic commands ###
