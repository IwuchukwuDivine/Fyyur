"""empty message

Revision ID: 71272a4a2a5f
Revises: 9de913306a22
Create Date: 2022-08-13 13:50:11.746391

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71272a4a2a5f'
down_revision = '9de913306a22'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artist', sa.Column('created_on', sa.DateTime(), nullable=False))
    op.add_column('venue', sa.Column('created_on', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venue', 'created_on')
    op.drop_column('artist', 'created_on')
    # ### end Alembic commands ###
