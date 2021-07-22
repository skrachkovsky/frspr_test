"""create tables

Revision ID: 9a3a60f63098
Revises: 
Create Date: 2021-07-21 07:36:10.628013

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a3a60f63098'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'phones',
        sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column('fullname', sa.String(255), nullable=False),
        sa.Column('address', sa.String(255), nullable=False),
        sa.Column('phone', sa.BigInteger, nullable=False),
        sa.UniqueConstraint('fullname', 'address', 'phone', name='phones_uniq_1')
    )


def downgrade():
    op.drop_table('phones')
