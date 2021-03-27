"""Initial migration

Revision ID: 13ae875fdc72
Revises: 
Create Date: 2021-03-27 16:00:16.171961

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13ae875fdc72'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('auth0id', sa.String(64), index=True),
        sa.Column('last_seen', sa.DateTime)
    )
    op.create_table(
        'annotation',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('bookid', sa.Integer),
        sa.Column('open_char', sa.Integer),
        sa.Column('close_char', sa.Integer),
        sa.Column('text', sa.Text)
    )


def downgrade():
    op.drop_table('user')
    op.drop_table('annotation')
