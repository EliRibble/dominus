"""kingdom.creator

Revision ID: ef6fef5147b2
Revises: 4bf7eb25abfb
Create Date: 2016-10-20 20:44:45.583486

"""

# revision identifiers, used by Alembic.
revision = 'ef6fef5147b2'
down_revision = '4bf7eb25abfb'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.add_column('kingdom', sa.Column('creator', postgresql.UUID(as_uuid=True), nullable=False))

def downgrade():
    op.drop_column('kingdom', 'creator')
