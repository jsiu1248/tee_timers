"""empty message

Revision ID: 0960a29c9551
Revises: 514b815e130f
Create Date: 2023-04-30 22:49:06.980497

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0960a29c9551'
down_revision = '514b815e130f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'actions', ['id'])
    op.create_unique_constraint(None, 'actions', ['action'])
    op.create_unique_constraint(None, 'badge', ['id'])
    op.create_unique_constraint(None, 'badge', ['name'])
    op.create_unique_constraint(None, 'golflog', ['id'])
    op.create_unique_constraint(None, 'user_badges', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user_badges', type_='unique')
    op.drop_constraint(None, 'golflog', type_='unique')
    op.drop_constraint(None, 'badge', type_='unique')
    op.drop_constraint(None, 'badge', type_='unique')
    op.drop_constraint(None, 'actions', type_='unique')
    op.drop_constraint(None, 'actions', type_='unique')
    # ### end Alembic commands ###
