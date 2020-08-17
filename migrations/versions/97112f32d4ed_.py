"""empty message

Revision ID: 97112f32d4ed
Revises: 2cfb2b0977db
Create Date: 2019-07-31 11:52:41.905557

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97112f32d4ed'
down_revision = '2cfb2b0977db'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('board_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['board_id'], ['board.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post')
    # ### end Alembic commands ###