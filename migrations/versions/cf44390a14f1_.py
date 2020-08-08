"""empty message

Revision ID: cf44390a14f1
Revises: 
Create Date: 2020-08-08 14:42:36.834587

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf44390a14f1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dishes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('picture', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('order_sum', sa.Float(), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('mail', sa.String(), nullable=False),
    sa.Column('phone', sa.String(), nullable=False),
    sa.Column('adress', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('mail', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('mail')
    )
    op.create_table('orders_asso',
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('dish_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['dish_id'], ['dishes.id'], ),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('orders_asso')
    op.drop_table('users')
    op.drop_table('orders')
    op.drop_table('dishes')
    op.drop_table('categories')
    # ### end Alembic commands ###