"""add rating creator

Revision ID: 2653b4d2dde6
Revises: 96ca40f7c6c2
Create Date: 2016-10-27 15:16:02.233187

"""

# revision identifiers, used by Alembic.
revision = '2653b4d2dde6'
down_revision = '96ca40f7c6c2'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.add_column('kingdomrating', sa.Column('creator', postgresql.UUID(as_uuid=True), nullable=False))
    op.create_foreign_key(op.f('fk_kingdomrating_user_creator'), 'kingdomrating', 'user', ['creator'], ['uuid'])


def downgrade():
    op.drop_constraint(op.f('fk_kingdomrating_user_creator'), 'kingdomrating', type_='foreignkey')
    op.drop_column('kingdomrating', 'creator')
