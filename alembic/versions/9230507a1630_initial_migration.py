"""Initial migration

Revision ID: 9230507a1630
Revises: 
Create Date: 2021-06-05 12:14:47.258001

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9230507a1630'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('annotation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('bookid', sa.Integer(), nullable=True),
    sa.Column('author', sa.String(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('edit',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('annotation_id', sa.Integer(), nullable=True),
    sa.Column('text', sa.Text(), nullable=True),
    sa.Column('editor', sa.String(), nullable=True),
    sa.Column('start', sa.Integer(), nullable=True),
    sa.Column('end', sa.Integer(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['annotation_id'], ['annotation.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_edit_annotation_id'), 'edit', ['annotation_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_edit_annotation_id'), table_name='edit')
    op.drop_table('edit')
    op.drop_table('annotation')
    # ### end Alembic commands ###