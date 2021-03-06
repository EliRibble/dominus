"""kingdom play creator and comments

Revision ID: d8f4cb2ea5a0
Revises: e95a53a6c0f3
Create Date: 2016-11-02 13:23:36.066512

"""

# revision identifiers, used by Alembic.
revision = 'd8f4cb2ea5a0'
down_revision = 'e95a53a6c0f3'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('kingdomcomment', sa.Column('content', sa.String(length=2048), nullable=False))
    op.drop_column('kingdomcomment', 'author')
    op.add_column('kingdomplay', sa.Column('comments', sa.String(length=2048), nullable=True))
    op.add_column('kingdomplay', sa.Column('creator', postgresql.UUID(as_uuid=True), nullable=False))
    op.add_column('kingdomplay', sa.Column('rating', sa.Integer(), nullable=False))
    op.create_foreign_key(op.f('fk_kingdomplay_user_creator'), 'kingdomplay', 'user', ['creator'], ['uuid'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('fk_kingdomplay_user_creator'), 'kingdomplay', type_='foreignkey')
    op.drop_column('kingdomplay', 'rating')
    op.drop_column('kingdomplay', 'creator')
    op.drop_column('kingdomplay', 'comments')
    op.add_column('kingdomcomment', sa.Column('author', sa.VARCHAR(length=256), autoincrement=False, nullable=False))
    op.drop_column('kingdomcomment', 'content')
    ### end Alembic commands ###
