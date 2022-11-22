"""empty message

Revision ID: ab32fff8ad7d
Revises: 7df739307b38
Create Date: 2022-11-21 18:28:03.786480

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab32fff8ad7d'
down_revision = '7df739307b38'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('golf_course',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('city', sa.String(length=64), nullable=True),
    sa.Column('state', sa.String(length=64), nullable=True),
    sa.Column('course', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('userprofile',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('gender_id', sa.Integer(), nullable=True),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('city_id', sa.Integer(), nullable=True),
    sa.Column('state_id', sa.Integer(), nullable=True),
    sa.Column('bio', sa.Text(), nullable=True),
    sa.Column('day_id', sa.Integer(), nullable=True),
    sa.Column('time_of_day_id', sa.Integer(), nullable=True),
    sa.Column('ride_or_walk_id', sa.Integer(), nullable=True),
    sa.Column('handicap_id', sa.Integer(), nullable=True),
    sa.Column('smoking_id', sa.Integer(), nullable=True),
    sa.Column('drinking_id', sa.Integer(), nullable=True),
    sa.Column('playing_type_id', sa.Integer(), nullable=True),
    sa.Column('golf_course_id', sa.Integer(), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['city_id'], ['city.id'], ),
    sa.ForeignKeyConstraint(['day_id'], ['day.id'], ),
    sa.ForeignKeyConstraint(['drinking_id'], ['drinking.id'], ),
    sa.ForeignKeyConstraint(['gender_id'], ['gender.id'], ),
    sa.ForeignKeyConstraint(['golf_course_id'], ['golf_course.id'], ),
    sa.ForeignKeyConstraint(['handicap_id'], ['handicap.id'], ),
    sa.ForeignKeyConstraint(['id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['playing_type_id'], ['playing_type.id'], ),
    sa.ForeignKeyConstraint(['ride_or_walk_id'], ['ride_or_walk.id'], ),
    sa.ForeignKeyConstraint(['smoking_id'], ['smoking.id'], ),
    sa.ForeignKeyConstraint(['state_id'], ['state.id'], ),
    sa.ForeignKeyConstraint(['time_of_day_id'], ['time_of_day.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('user_profile')
    op.drop_table('golfcourse')
    op.alter_column('city', 'id',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=True)
    op.drop_column('city', 'city_id')
    op.add_column('ride_or_walk', sa.Column('ride_or_walk_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'ride_or_walk', 'userprofile', ['ride_or_walk_id'], ['ride_or_walk_id'])
    op.alter_column('state', 'id',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=True)
    op.drop_column('state', 'state_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('state', sa.Column('state_id', sa.VARCHAR(length=64), nullable=False))
    op.alter_column('state', 'id',
               existing_type=sa.INTEGER(),
               nullable=True,
               autoincrement=True)
    op.drop_constraint(None, 'ride_or_walk', type_='foreignkey')
    op.drop_column('ride_or_walk', 'ride_or_walk_id')
    op.add_column('city', sa.Column('city_id', sa.VARCHAR(length=64), nullable=False))
    op.alter_column('city', 'id',
               existing_type=sa.INTEGER(),
               nullable=True,
               autoincrement=True)
    op.create_table('golfcourse',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('city', sa.VARCHAR(length=64), nullable=True),
    sa.Column('state', sa.VARCHAR(length=64), nullable=True),
    sa.Column('course', sa.VARCHAR(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_profile',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('gender_id', sa.INTEGER(), nullable=True),
    sa.Column('city_id', sa.INTEGER(), nullable=True),
    sa.Column('state_id', sa.INTEGER(), nullable=True),
    sa.Column('bio', sa.TEXT(), nullable=True),
    sa.Column('day_id', sa.INTEGER(), nullable=True),
    sa.Column('time_of_day_id', sa.INTEGER(), nullable=True),
    sa.Column('ride_or_walk_id', sa.INTEGER(), nullable=True),
    sa.Column('handicap_id', sa.INTEGER(), nullable=True),
    sa.Column('smoking_id', sa.INTEGER(), nullable=True),
    sa.Column('drinking_id', sa.INTEGER(), nullable=True),
    sa.Column('playing_type_id', sa.INTEGER(), nullable=True),
    sa.Column('last_seen', sa.DATETIME(), nullable=True),
    sa.Column('age', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('userprofile')
    op.drop_table('golf_course')
    # ### end Alembic commands ###
