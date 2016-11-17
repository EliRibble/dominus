"""add set owned

Revision ID: f06e0da1bdf4
Revises: 980fdee06558
Create Date: 2016-11-17 20:32:18.950479

"""

# revision identifiers, used by Alembic.
revision = 'f06e0da1bdf4'
down_revision = '980fdee06558'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.create_table('set_owned',
        sa.Column('uuid', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('created', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('deleted', sa.DateTime(), nullable=True),
        sa.Column('user', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('set', postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(['set'], ['set.uuid'], name=op.f('fk_set_owned_set_set')),
        sa.ForeignKeyConstraint(['user'], ['user.uuid'], name=op.f('fk_set_owned_user_user')),
        sa.PrimaryKeyConstraint('uuid', name=op.f('pk_set_owned'))
    )


def downgrade():
    op.drop_table('set_owned')
