"""updating column name

Revision ID: 7dd37ed381de
Revises: c0e7b966dfa7
Create Date: 2024-05-18 17:17:23.345483

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '7dd37ed381de'
down_revision: Union[str, None] = 'c0e7b966dfa7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('attachments', sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.drop_column('attachments', 'update_at')
    op.add_column('meanings', sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.drop_column('meanings', 'update_at')
    op.add_column('words', sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.drop_column('words', 'update_at')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('words', sa.Column('update_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True))
    op.drop_column('words', 'updated_at')
    op.add_column('meanings', sa.Column('update_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True))
    op.drop_column('meanings', 'updated_at')
    op.add_column('attachments', sa.Column('update_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True))
    op.drop_column('attachments', 'updated_at')
    # ### end Alembic commands ###
