import sqlalchemy as sa

from ..database import db

__all__ = 'phones',


phones = sa.Table(
    'phones', db.metadata,
    sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
    sa.Column('fullname', sa.String(255), nullable=False),
    sa.Column('address', sa.String(255), nullable=False),
    sa.Column('phone', sa.String(15), nullable=False),
    sa.UniqueConstraint('fullname', 'address', 'phone', name='phones_uniq_1')
)
