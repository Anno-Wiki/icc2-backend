"""Add Edit table

Revision ID: 2f0cd0152e0b
Revises: 13ae875fdc72
Create Date: 2021-04-03 15:32:06.371647

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f0cd0152e0b'
down_revision = '13ae875fdc72'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('annotation', 'text')
    op.drop_table('user')
    op.add_column('annotation', sa.Column('author', sa.String))
    op.create_table(
        'edit',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('annotation_id', sa.Integer, sa.ForeignKey('annotation.id')),
        sa.Column('text', sa.Text),
        sa.Column('editor', sa.String)
    )


def downgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('auth0id', sa.String(64), index=True),
        sa.Column('last_seen', sa.DateTime)
    )
    op.drop_column('annotation', 'author')
    op.add_column('annotation', sa.Column('text', sa.Text))
