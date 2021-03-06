"""empty message

Revision ID: c5ccf9aaaeb9
Revises: 7248a693ccd5
Create Date: 2019-07-30 15:11:45.298243

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c5ccf9aaaeb9'
down_revision = '7248a693ccd5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('banner_model',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('image_url', sa.String(length=100), nullable=False),
    sa.Column('link_url', sa.String(length=100), nullable=False),
    sa.Column('priority', sa.Integer(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('banner_model')
    # ### end Alembic commands ###
