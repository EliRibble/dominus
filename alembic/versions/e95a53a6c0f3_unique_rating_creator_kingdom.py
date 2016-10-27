"""unique rating creator kingdom

Revision ID: e95a53a6c0f3
Revises: 2653b4d2dde6
Create Date: 2016-10-27 15:32:15.269869

"""

# revision identifiers, used by Alembic.
revision = 'e95a53a6c0f3'
down_revision = '2653b4d2dde6'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_unique_constraint('uq_rating_kingdom_creator', 'kingdomrating', ['kingdom', 'creator'])


def downgrade():
    op.drop_constraint('uq_rating_kingdom_creator', 'kingdomrating', type_='unique')
