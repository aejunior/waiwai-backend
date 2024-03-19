"""feat: initial commit

Revision ID: 88cc2ed900c4
Revises: 
Create Date: 2024-03-18 23:45:58.387980

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '88cc2ed900c4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('category', sa.String(length=20), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('category')
    )
    op.create_table('references',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('reference', sa.String(length=280), nullable=False),
    sa.Column('url', sa.String(length=2048), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('reference')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=15), nullable=False),
    sa.Column('last_name', sa.String(length=15), nullable=False),
    sa.Column('full_name', sa.String(length=31), nullable=False),
    sa.Column('email', sa.String(length=319), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.Column('permission', sa.Enum('GUEST', 'USER', 'ADMIN', name='permissiontype'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('version',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('version', sa.NUMERIC(), nullable=False),
    sa.Column('words', postgresql.TIMESTAMP(), nullable=False),
    sa.Column('meanings', postgresql.TIMESTAMP(), nullable=False),
    sa.Column('categories', postgresql.TIMESTAMP(), nullable=False),
    sa.Column('references', postgresql.TIMESTAMP(), nullable=False),
    sa.Column('attachments', postgresql.TIMESTAMP(), nullable=False),
    sa.Column('users', postgresql.TIMESTAMP(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('words',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('word', sa.String(length=50), nullable=False),
    sa.Column('phonemic', sa.String(length=120), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('update_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('word')
    )
    op.create_table('attachments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.Uuid(), nullable=False),
    sa.Column('filename', sa.String(length=255), nullable=False),
    sa.Column('filedir', sa.String(length=255), nullable=False),
    sa.Column('url', sa.String(length=255), nullable=False),
    sa.Column('content_type', sa.String(length=20), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('update_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('word_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['word_id'], ['words.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('url')
    )
    op.create_table('meanings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('meaning', sa.String(length=200), nullable=False),
    sa.Column('comment', sa.String(length=256), nullable=True),
    sa.Column('chapter_id', sa.Integer(), nullable=True),
    sa.Column('entry_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('update_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('word_id', sa.Integer(), nullable=False),
    sa.Column('reference_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['reference_id'], ['references.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['word_id'], ['words.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('word_category',
    sa.Column('word_id', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.ForeignKeyConstraint(['word_id'], ['words.id'], ),
    sa.PrimaryKeyConstraint('word_id', 'category_id')
    )

    triggers = [
        'CREATE TRIGGER on_attachments AFTER INSERT OR UPDATE OR DELETE ON waiwaitapota.public."attachments"'
        "FOR EACH ROW EXECUTE PROCEDURE version_update('attachments');",
        'CREATE TRIGGER on_categories AFTER INSERT OR UPDATE OR DELETE ON waiwaitapota.public."categories"'
        "FOR EACH ROW EXECUTE PROCEDURE version_update('categories');",
        'CREATE TRIGGER on_words AFTER INSERT OR UPDATE OR DELETE ON waiwaitapota.public."words"'
        "FOR EACH ROW EXECUTE PROCEDURE version_update('words');",
        'CREATE TRIGGER on_users AFTER INSERT OR UPDATE OR DELETE ON waiwaitapota.public."users"'
        "FOR EACH ROW EXECUTE PROCEDURE version_update('users');",
        'CREATE TRIGGER on_references AFTER INSERT OR UPDATE OR DELETE ON waiwaitapota.public."references"'
        "FOR EACH ROW EXECUTE PROCEDURE version_update('references');",
        'CREATE TRIGGER on_meanings AFTER INSERT OR UPDATE OR DELETE ON waiwaitapota.public."meanings"'
        "FOR EACH ROW EXECUTE PROCEDURE version_update('meanings');"]
    for trigger in triggers:
        op.execute(trigger)

    op.execute(
        """
        create or replace function version_update() RETURNS trigger
        language plpgsql
        as $$
            declare
                version_timestamp timestamp;
                sql_base varchar(200);
            begin
            version_timestamp := now();
            if not exists(select id from waiwaitapota.public.version) then
                insert into waiwaitapota.public.version (version, words, meanings, categories, "references", attachments, users)
                select 1, version_timestamp, version_timestamp, version_timestamp, version_timestamp, version_timestamp, version_timestamp;
            end if;
            sql_base = 'update waiwaitapota.public.version set "@version" = $1, version = vv.version+0.1 from waiwaitapota.public.version vv';
            sql_base = replace(sql_base, '@version', TG_ARGV[0]);
            EXECUTE sql_base USING version_timestamp;
            RETURN NEW;
        end;
        $$;
        """
    )


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###

    triggers = [
        'DROP TRIGGER IF EXISTS on_attachments;',
        'DROP TRIGGER IF EXISTS on_categories;',
        'DROP TRIGGER IF EXISTS on_words;',
        'DROP TRIGGER IF EXISTS on_users;',
        'DROP TRIGGER IF EXISTS on_references;',
        'DROP TRIGGER IF EXISTS on_meanings;']

    for trigger in triggers:
        op.execute(trigger)

    sa.execute('DROP TRIGGER IF EXISTS on_attachments;')
    sa.execute('DROP TRIGGER IF EXISTS on_categories;')
    sa.execute('DROP TRIGGER IF EXISTS on_words;')
    sa.execute('DROP TRIGGER IF EXISTS on_users;')
    sa.execute('DROP TRIGGER IF EXISTS on_references;')
    sa.execute('DROP TRIGGER IF EXISTS on_meanings;')

    op.drop_table('word_category')
    op.drop_table('meanings')
    op.drop_table('attachments')
    op.drop_table('words')
    op.drop_table('version')
    op.drop_table('users')
    op.drop_table('references')
    op.drop_table('categories')
    op.execute('drop type permissiontype;')
    op.execute('drop function version_update;')
    # ### end Alembic commands ###
