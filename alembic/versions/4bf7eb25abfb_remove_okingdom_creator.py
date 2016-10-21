"""remove okingdom creator

Revision ID: 4bf7eb25abfb
Revises: 967c795c9bfd
Create Date: 2016-10-20 20:43:28.591371

"""

# revision identifiers, used by Alembic.
revision = '4bf7eb25abfb'
down_revision = '967c795c9bfd'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_column('kingdom', 'creator')


def downgrade():
    op.add_column('kingdom', sa.Column('creator', sa.VARCHAR(length=256), autoincrement=False, nullable=False))
