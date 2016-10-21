"""user table

Revision ID: 967c795c9bfd
Revises: 39a72c144eaa
Create Date: 2016-10-20 20:06:23.788227

"""

# revision identifiers, used by Alembic.
revision = '967c795c9bfd'
down_revision = '39a72c144eaa'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.create_table('user',
        sa.Column('uuid', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('created', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('deleted', sa.DateTime(), nullable=True),
        sa.Column('username', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=128), nullable=False),
        sa.PrimaryKeyConstraint('uuid', name=op.f('pk_user')),
        sa.UniqueConstraint('username', name=op.f('uq_user_username'))
    )


def downgrade():
    op.drop_table('user')
