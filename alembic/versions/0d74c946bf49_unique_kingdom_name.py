"""unique kingdom name

Revision ID: 0d74c946bf49
Revises: d8f4cb2ea5a0
Create Date: 2016-11-05 15:41:31.614932

"""

# revision identifiers, used by Alembic.
revision = '0d74c946bf49'
down_revision = 'd8f4cb2ea5a0'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_unique_constraint(op.f('uq_kingdom_name'), 'kingdom', ['name'])


def downgrade():
    op.drop_constraint(op.f('uq_kingdom_name'), 'kingdom', type_='unique')
