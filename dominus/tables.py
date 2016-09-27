import chryso.schema
import sqlalchemy

metadata = chryso.schema.metadata

Set = chryso.schema.table('set',
    sqlalchemy.Column('name', sqlalchemy.String(256), nullable=False),
)

Cards = chryso.schema.table('card',
    sqlalchemy.Column('name', sqlalchemy.String(256), nullable=False),
    sqlalchemy.Column('text', sqlalchemy.String(1024), nullable=False),
    sqlalchemy.Column('set', None, sqlalchemy.ForeignKey('set.uuid'), nullable=False),
)
