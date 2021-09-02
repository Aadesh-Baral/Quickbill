"""'initial'

Revision ID: 86900fdfcf6f
Revises: 
Create Date: 2021-02-15 17:29:59.422385

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '86900fdfcf6f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('firstname', sa.Text(), nullable=True),
    sa.Column('lastname', sa.Text(), nullable=True),
    sa.Column('username', sa.Text(), nullable=True),
    sa.Column('password_hash', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_admin_username'), 'admin', ['username'], unique=True)
    op.create_table('costumer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('firstname', sa.String(), nullable=False),
    sa.Column('lastname', sa.String(), nullable=False),
    sa.Column('companyname', sa.String(), nullable=True),
    sa.Column('role', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('primary_no', sa.String(), nullable=False),
    sa.Column('secondary_no', sa.String(), nullable=True),
    sa.Column('address', sa.Text(), nullable=True),
    sa.Column('pan_no', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_costumer_companyname'), 'costumer', ['companyname'], unique=True)
    op.create_table('items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('item_name', sa.Text(), nullable=True),
    sa.Column('item_category', sa.Text(), nullable=True),
    sa.Column('item_brand', sa.Text(), nullable=True),
    sa.Column('item_quantity', sa.Integer(), nullable=True),
    sa.Column('item_price', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('purchase',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('admin_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('item', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('alternate_quantity', sa.String(), nullable=False),
    sa.Column('quantity', sa.String(), nullable=False),
    sa.Column('rate', sa.String(), nullable=False),
    sa.Column('per', sa.String(), nullable=False),
    sa.Column('amount', sa.String(), nullable=False),
    sa.Column('total_amount', sa.Integer(), nullable=False),
    sa.Column('paid_amount', sa.Integer(), nullable=True),
    sa.Column('remaning_amount', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['admin_id'], ['admin.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sales',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('admin_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('item', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('alternate_quantity', sa.String(), nullable=False),
    sa.Column('quantity', sa.String(), nullable=False),
    sa.Column('rate', sa.String(), nullable=False),
    sa.Column('per', sa.String(), nullable=False),
    sa.Column('amount', sa.String(), nullable=False),
    sa.Column('total_amount', sa.Integer(), nullable=False),
    sa.Column('discount', sa.Integer(), nullable=True),
    sa.Column('paid_amount', sa.Integer(), nullable=True),
    sa.Column('remaning_amount', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['admin_id'], ['admin.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sales')
    op.drop_table('purchase')
    op.drop_table('items')
    op.drop_index(op.f('ix_costumer_companyname'), table_name='costumer')
    op.drop_table('costumer')
    op.drop_index(op.f('ix_admin_username'), table_name='admin')
    op.drop_table('admin')
    # ### end Alembic commands ###
