"""initial hero table creation

Revision ID: dde7e0d4e9c7
Revises: 
Create Date: 2022-10-08 18:52:43.173777

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dde7e0d4e9c7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('heroes',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('randomable', sa.Boolean(), nullable=False),
    sa.Column('hero_type', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('heroes')
    # ### end Alembic commands ###