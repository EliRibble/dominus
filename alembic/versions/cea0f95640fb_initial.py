"""initial

Revision ID: cea0f95640fb
Revises: 
Create Date: 2016-09-27 13:54:12.311606

"""

# revision identifiers, used by Alembic.
revision = 'cea0f95640fb'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('set',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('created', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=256), nullable=False),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_set'))
    )
    op.create_table('card',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('created', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=256), nullable=False),
    sa.Column('text', sa.String(length=1024), nullable=False),
    sa.Column('set', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['set'], ['set.uuid'], name=op.f('fk_card_set_set')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_card'))
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('card')
    op.drop_table('set')
    ### end Alembic commands ###
