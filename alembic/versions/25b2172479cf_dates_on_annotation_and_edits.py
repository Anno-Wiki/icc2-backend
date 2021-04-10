"""dates on annotation and edits

Revision ID: 25b2172479cf
Revises: 2f0cd0152e0b
Create Date: 2021-04-10 10:49:14.417350

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25b2172479cf'
down_revision = '2f0cd0152e0b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('annotation', sa.Column('created', sa.DateTime))
    op.add_column('edit', sa.Column('created', sa.DateTime))


def downgrade():
    op.drop_column('annotation', 'created')
    op.drop_column('edit', 'created')
