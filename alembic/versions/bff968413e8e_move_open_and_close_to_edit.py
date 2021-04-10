"""move open and close to edit

Revision ID: bff968413e8e
Revises: 25b2172479cf
Create Date: 2021-04-10 10:57:03.983871

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bff968413e8e'
down_revision = '25b2172479cf'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('annotation', 'open_char')
    op.drop_column('annotation', 'close_char')
    op.add_column('edit', sa.Column('open', sa.Integer))
    op.add_column('edit', sa.Column('close', sa.Integer))


def downgrade():
    op.drop_column('edit', 'open')
    op.drop_column('edit', 'close')
    op.add_column('annotation', sa.Column('open_char', sa.Integer))
    op.add_column('annotation', sa.Column('close_char', sa.Integer))
