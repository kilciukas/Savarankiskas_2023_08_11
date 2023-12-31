"""a

Revision ID: ff3f3a5e6617
Revises: 
Create Date: 2023-08-11 10:28:45.073869

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff3f3a5e6617'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('studentai',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('vardas', sa.String(length=80), nullable=False),
    sa.Column('pavarde', sa.String(length=120), nullable=False),
    sa.Column('el_pastas', sa.String(length=40), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('studentai')
    # ### end Alembic commands ###
