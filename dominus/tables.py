import chryso.schema
import sqlalchemy
import sqlalchemy.dialects.postgresql

import dominus.constants

metadata = chryso.schema.metadata

User = chryso.schema.table('user',
    sqlalchemy.Column('username',      sqlalchemy.String(255), nullable=False, unique=True),
    sqlalchemy.Column('password_hash', sqlalchemy.String(128), nullable=False),
)

Set = chryso.schema.table('set',
    sqlalchemy.Column('name', sqlalchemy.String(256), nullable=False),
)

Card = chryso.schema.table('card',
    sqlalchemy.Column('cost_in_debt', sqlalchemy.Integer(), nullable=False),
    sqlalchemy.Column('cost_in_treasure', sqlalchemy.Integer(), nullable=False),
    sqlalchemy.Column('is_in_supply', sqlalchemy.Boolean(), nullable=False),
    sqlalchemy.Column('name', sqlalchemy.String(256), nullable=False),
    sqlalchemy.Column('set', None, sqlalchemy.ForeignKey('set.uuid'), nullable=False),
    sqlalchemy.Column('text', sqlalchemy.String(1024), nullable=False),
)

CardTypeName = sqlalchemy.dialects.postgresql.ENUM(*[str(x) for x in dominus.constants.CardType], name='card_type_name')
CardType = chryso.schema.table('cardtype',
    sqlalchemy.Column('name', CardTypeName, nullable=False),
    sqlalchemy.Column('card', None, sqlalchemy.ForeignKey('card.uuid'), nullable=False),
)

Kingdom = chryso.schema.table('kingdom',
    sqlalchemy.Column('creator', None, sqlalchemy.ForeignKey('user.uuid'), nullable=False),
    sqlalchemy.Column('has_colony', sqlalchemy.Boolean(), server_default='FALSE', nullable=False),
    sqlalchemy.Column('has_platinum', sqlalchemy.Boolean(), server_default='FALSE', nullable=False),
    sqlalchemy.Column('has_shelters', sqlalchemy.Boolean(), server_default='FALSE', nullable=False),
    sqlalchemy.Column('name', sqlalchemy.String(256), nullable=False, unique=True),
)

KingdomCard = chryso.schema.table('kingdomcard',
    sqlalchemy.Column('kingdom', None, sqlalchemy.ForeignKey('kingdom.uuid'), nullable=False),
    sqlalchemy.Column('card', None, sqlalchemy.ForeignKey('card.uuid'), nullable=False),
)

KingdomComment = chryso.schema.table('kingdomcomment',
    sqlalchemy.Column('kingdom', None, sqlalchemy.ForeignKey('kingdom.uuid'), nullable=False),
    sqlalchemy.Column('content', sqlalchemy.String(2048), nullable=False),
)

KingdomRating = chryso.schema.table('kingdomrating',
    sqlalchemy.Column('kingdom', None, sqlalchemy.ForeignKey('kingdom.uuid'), nullable=False),
    sqlalchemy.Column('rating', sqlalchemy.Integer(), nullable=False),
    sqlalchemy.Column('creator', None, sqlalchemy.ForeignKey('user.uuid'), nullable=False),
    sqlalchemy.UniqueConstraint('kingdom', 'creator', name='uq_rating_kingdom_creator'),
)

KingdomPlay = chryso.schema.table('kingdomplay',
    sqlalchemy.Column('comments', sqlalchemy.String(2048), nullable=True),
    sqlalchemy.Column('creator', None, sqlalchemy.ForeignKey('user.uuid'), nullable=False),
    sqlalchemy.Column('kingdom', None, sqlalchemy.ForeignKey('kingdom.uuid'), nullable=False),
    sqlalchemy.Column('player_count', sqlalchemy.Integer(), nullable=False),
    sqlalchemy.Column('rating', sqlalchemy.Integer(), nullable=False),
)
