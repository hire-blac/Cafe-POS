"""stores

Revision ID: 8a351183da70
Revises: 74915bf3d538
Create Date: 2024-03-29 08:35:38.075314

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8a351183da70'
down_revision: Union[str, None] = '74915bf3d538'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_table('store profiles')
    with op.batch_alter_table('categories', schema=None) as batch_op:
        batch_op.add_column(sa.Column('store_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('company_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('company', 'companies', ['company_id'], ['id'])
        batch_op.create_foreign_key('store', 'stores', ['store_id'], ['id'])

    with op.batch_alter_table('customers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('store_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('company_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('store', 'stores', ['store_id'], ['id'])
        batch_op.create_foreign_key('company', 'companies', ['company_id'], ['id'])

    with op.batch_alter_table('deliveries', schema=None) as batch_op:
        batch_op.add_column(sa.Column('store_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('company_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('company', 'companies', ['company_id'], ['id'])
        batch_op.create_foreign_key('store', 'stores', ['store_id'], ['id'])

    with op.batch_alter_table('invoices', schema=None) as batch_op:
        batch_op.add_column(sa.Column('store_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('company_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('store', 'stores', ['store_id'], ['id'])
        batch_op.create_foreign_key('company', 'companies', ['company_id'], ['id'])

    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.add_column(sa.Column('store_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('company_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('store', 'stores', ['store_id'], ['id'])
        batch_op.create_foreign_key('company', 'companies', ['company_id'], ['id'])

    with op.batch_alter_table('ordered_item', schema=None) as batch_op:
        batch_op.add_column(sa.Column('store_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('company_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('company', 'companies', ['company_id'], ['id'])
        batch_op.create_foreign_key('store', 'stores', ['store_id'], ['id'])

    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.add_column(sa.Column('store_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('company_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('company', 'companies', ['company_id'], ['id'])
        batch_op.create_foreign_key('store', 'stores', ['store_id'], ['id'])

    with op.batch_alter_table('suppliers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('store_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('company_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('company', 'companies', ['company_id'], ['id'])
        batch_op.create_foreign_key('store', 'stores', ['store_id'], ['id'])

    with op.batch_alter_table('transactions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('store_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('company_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('store', 'stores', ['store_id'], ['id'])
        batch_op.create_foreign_key('company', 'companies', ['company_id'], ['id'])

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('store_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('company_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('store', 'stores', ['store_id'], ['id'])
        batch_op.create_foreign_key('company', 'companies', ['company_id'], ['id'])

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint('company', type_='foreignkey')
        batch_op.drop_constraint('store', type_='foreignkey')
        batch_op.drop_column('company_id')
        batch_op.drop_column('store_id')

    with op.batch_alter_table('transactions', schema=None) as batch_op:
        batch_op.drop_constraint('company', type_='foreignkey')
        batch_op.drop_constraint('store', type_='foreignkey')
        batch_op.drop_column('company_id')
        batch_op.drop_column('store_id')

    with op.batch_alter_table('suppliers', schema=None) as batch_op:
        batch_op.drop_constraint('company', type_='foreignkey')
        batch_op.drop_constraint('store', type_='foreignkey')
        batch_op.drop_column('company_id')
        batch_op.drop_column('store_id')

    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.drop_constraint('company', type_='foreignkey')
        batch_op.drop_constraint('store', type_='foreignkey')
        batch_op.drop_column('company_id')
        batch_op.drop_column('store_id')

    with op.batch_alter_table('ordered_item', schema=None) as batch_op:
        batch_op.drop_constraint('company', type_='foreignkey')
        batch_op.drop_constraint('store', type_='foreignkey')
        batch_op.drop_column('company_id')
        batch_op.drop_column('store_id')

    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.drop_constraint('company', type_='foreignkey')
        batch_op.drop_constraint('store', type_='foreignkey')
        batch_op.drop_column('company_id')
        batch_op.drop_column('store_id')

    with op.batch_alter_table('invoices', schema=None) as batch_op:
        batch_op.drop_constraint('company', type_='foreignkey')
        batch_op.drop_constraint('store', type_='foreignkey')
        batch_op.drop_column('company_id')
        batch_op.drop_column('store_id')

    with op.batch_alter_table('deliveries', schema=None) as batch_op:
        batch_op.drop_constraint('company', type_='foreignkey')
        batch_op.drop_constraint('store', type_='foreignkey')
        batch_op.drop_column('company_id')
        batch_op.drop_column('store_id')

    with op.batch_alter_table('customers', schema=None) as batch_op:
        batch_op.drop_constraint('company', type_='foreignkey')
        batch_op.drop_constraint('store', type_='foreignkey')
        batch_op.drop_column('company_id')
        batch_op.drop_column('store_id')

    with op.batch_alter_table('categories', schema=None) as batch_op:
        batch_op.drop_constraint('company', type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('company_id')
        batch_op.drop_column('store_id')

    op.create_table('store profiles',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('address', sa.VARCHAR(), nullable=False),
    sa.Column('tax_id', sa.VARCHAR(), nullable=False),
    sa.Column('phone', sa.VARCHAR(), nullable=False),
    sa.Column('logo_url', sa.VARCHAR(), nullable=True),
    sa.Column('company_name', sa.VARCHAR(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###