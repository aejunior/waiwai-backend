"""feat: relationship usercategory

Revision ID: 3c94eb4eb3eb
Revises: b3c02bb93acb
Create Date: 2024-02-18 14:02:16.159719

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3c94eb4eb3eb'
down_revision: Union[str, None] = 'b3c02bb93acb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('categories', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'categories', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'categories', type_='foreignkey')
    op.drop_column('categories', 'user_id')
    # ### end Alembic commands ###
