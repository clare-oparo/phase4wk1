"""initial migration

Revision ID: 034f1f51d3a9
Revises: 
Create Date: 2024-04-09 09:23:17.103690

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '034f1f51d3a9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pizza',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('ingredients', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('restaurant',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('address', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('restaurant_pizza',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('restaurant_id', sa.Integer(), nullable=False),
    sa.Column('pizza_id', sa.Integer(), nullable=False),
    sa.CheckConstraint('price >= 1 AND price <= 30', name='price_check'),
    sa.ForeignKeyConstraint(['pizza_id'], ['pizza.id'], ),
    sa.ForeignKeyConstraint(['restaurant_id'], ['restaurant.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('restaurant_pizza')
    op.drop_table('restaurant')
    op.drop_table('pizza')
    # ### end Alembic commands ###
