"""mark recommended kingdoms

Revision ID: 980fdee06558
Revises: 2548bcf4ec11
Create Date: 2016-11-07 14:48:56.383817

"""

# revision identifiers, used by Alembic.
revision = '980fdee06558'
down_revision = '2548bcf4ec11'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('kingdom', sa.Column('is_recommended', sa.Boolean(), server_default='FALSE', nullable=False))


def downgrade():
    op.drop_column('kingdom', 'is_recommended')
