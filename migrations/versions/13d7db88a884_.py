"""empty message

Revision ID: 13d7db88a884
Revises: 
Create Date: 2023-11-16 01:35:26.200913

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13d7db88a884'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('usuario_produccion',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('primer_nombre', sa.String(length=50), nullable=True),
    sa.Column('apellido', sa.String(length=50), nullable=True),
    sa.Column('nombre', sa.String(length=50), nullable=True),
    sa.Column('compensacion_unidad', sa.Float(), nullable=True),
    sa.Column('compensacion_paquete', sa.Float(), nullable=True),
    sa.Column('cantidad_total', sa.Integer(), nullable=True),
    sa.Column('fecha', sa.DateTime(), nullable=True),
    sa.Column('precio', sa.Integer(), nullable=True),
    sa.Column('nombre_rol', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('usuario_produccion')
    # ### end Alembic commands ###
