"""empty message

Revision ID: 606caf1485eb
Revises: 8b57e0b5c0b6
Create Date: 2022-11-12 13:32:07.408756

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '606caf1485eb'
down_revision = '8b57e0b5c0b6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('comment_html', sa.Text(), nullable=True),
    sa.Column('slug', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('slug')
    )
    op.create_index(op.f('ix_comments_timestamp'), 'comments', ['timestamp'], unique=False)
    op.drop_index('ix_compositions_timestamp', table_name='compositions')
    op.drop_table('compositions')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('compositions',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.VARCHAR(length=64), nullable=True),
    sa.Column('description', sa.TEXT(), nullable=True),
    sa.Column('timestamp', sa.DATETIME(), nullable=True),
    sa.Column('description_html', sa.TEXT(), nullable=True),
    sa.Column('slug', sa.VARCHAR(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('slug')
    )
    op.create_index('ix_compositions_timestamp', 'compositions', ['timestamp'], unique=False)
    op.drop_index(op.f('ix_comments_timestamp'), table_name='comments')
    op.drop_table('comments')
    # ### end Alembic commands ###