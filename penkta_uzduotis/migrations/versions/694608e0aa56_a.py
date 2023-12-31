"""a

Revision ID: 694608e0aa56
Revises: 
Create Date: 2023-08-11 10:39:40.940271

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '694608e0aa56'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('darbuotojas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('vardas', sa.String(), nullable=True),
    sa.Column('pavarde', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('departamentas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pavadinimas', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('darbuotojas_departamentas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('darbuotojo_id', sa.Integer(), nullable=True),
    sa.Column('departamento_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['darbuotojo_id'], ['darbuotojas.id'], ),
    sa.ForeignKeyConstraint(['departamento_id'], ['departamentas.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('darbuotojas_departamentas')
    op.drop_table('departamentas')
    op.drop_table('darbuotojas')
    # ### end Alembic commands ###
