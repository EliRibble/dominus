"""add creator

Revision ID: 96ca40f7c6c2
Revises: ef6fef5147b2
Create Date: 2016-10-27 15:14:18.031571

"""

# revision identifiers, used by Alembic.
revision = '96ca40f7c6c2'
down_revision = 'ef6fef5147b2'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.create_foreign_key(op.f('fk_kingdom_user_creator'), 'kingdom', 'user', ['creator'], ['uuid'])


def downgrade():
    op.drop_constraint(op.f('fk_kingdomrating_user_creator'), 'kingdomrating', type_='foreignkey')
