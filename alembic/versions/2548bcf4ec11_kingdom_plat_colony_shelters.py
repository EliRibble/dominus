"""kingdom plat colony shelters

Revision ID: 2548bcf4ec11
Revises: 0d74c946bf49
Create Date: 2016-11-05 21:34:29.551551

"""

# revision identifiers, used by Alembic.
revision = '2548bcf4ec11'
down_revision = '0d74c946bf49'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('kingdom', sa.Column('has_colony', sa.Boolean(), server_default='FALSE', nullable=False))
    op.add_column('kingdom', sa.Column('has_platinum', sa.Boolean(), server_default='FALSE', nullable=False))
    op.add_column('kingdom', sa.Column('has_shelters', sa.Boolean(), server_default='FALSE', nullable=False))


def downgrade():
    op.drop_column('kingdom', 'has_shelters')
    op.drop_column('kingdom', 'has_platinum')
    op.drop_column('kingdom', 'has_colony')
