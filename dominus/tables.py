import chryso.schema
import sqlalchemy

metadata = chryso.schema.metadata

Set = chryso.schema.table('set',
    sqlalchemy.Column('name', sqlalchemy.String(256), nullable=False),
)

Card = chryso.schema.table('card',
    sqlalchemy.Column('name', sqlalchemy.String(256), nullable=False),
    sqlalchemy.Column('set', None, sqlalchemy.ForeignKey('set.uuid'), nullable=False),
    sqlalchemy.Column('text', sqlalchemy.String(1024), nullable=False),
    sqlalchemy.Column('type', sqlalchemy.String(1024), nullable=False),
)

Kingdom = chryso.schema.table('kingdom',
    sqlalchemy.Column('name', sqlalchemy.String(256), nullable=False),
    sqlalchemy.Column('creator', sqlalchemy.String(256), nullable=False),
)

KingdomCard = chryso.schema.table('kingdomcard',
    sqlalchemy.Column('kingdom', None, sqlalchemy.ForeignKey('kingdom.uuid'), nullable=False),
    sqlalchemy.Column('card', None, sqlalchemy.ForeignKey('card.uuid'), nullable=False),
)

KingdomComment = chryso.schema.table('kingdomcomment',
    sqlalchemy.Column('kingdom', None, sqlalchemy.ForeignKey('kingdom.uuid'), nullable=False),
    sqlalchemy.Column('author', sqlalchemy.String(256), nullable=False),
)

KingdomRating = chryso.schema.table('kingdomrating',
    sqlalchemy.Column('kingdom', None, sqlalchemy.ForeignKey('kingdom.uuid'), nullable=False),
    sqlalchemy.Column('rating', sqlalchemy.Integer(), nullable=False),
)
