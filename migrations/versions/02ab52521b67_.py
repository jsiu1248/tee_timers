"""empty message

Revision ID: 02ab52521b67
Revises: 5ff51c832dcf
Create Date: 2022-11-21 18:56:42.502215

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02ab52521b67'
down_revision = '5ff51c832dcf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('city', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('days',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('day', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('drinkings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('drinking', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('genders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('gender', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('golf_courses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('city', sa.String(length=64), nullable=True),
    sa.Column('state', sa.String(length=64), nullable=True),
    sa.Column('course', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('handicaps',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('handicap', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('playing_types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('playing_type', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ride_or_walks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ride_or_walk', sa.String(length=64), nullable=True),
    sa.Column('ride_or_walk_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ride_or_walk_id'], ['userprofile.ride_or_walk_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('smokings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('smoking', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('states',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('state', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('time_of_days',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('time_of_day', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('ride_or_walk')
    op.drop_table('playing_type')
    op.drop_table('city')
    op.drop_table('handicap')
    op.drop_table('gender')
    op.drop_table('day')
    op.drop_table('golf_course')
    op.drop_table('time_of_day')
    op.drop_table('state')
    op.drop_table('smoking')
    op.drop_table('drinking')
    op.drop_constraint(None, 'userprofile', type_='foreignkey')
    op.drop_constraint(None, 'userprofile', type_='foreignkey')
    op.drop_constraint(None, 'userprofile', type_='foreignkey')
    op.drop_constraint(None, 'userprofile', type_='foreignkey')
    op.drop_constraint(None, 'userprofile', type_='foreignkey')
    op.drop_constraint(None, 'userprofile', type_='foreignkey')
    op.drop_constraint(None, 'userprofile', type_='foreignkey')
    op.drop_constraint(None, 'userprofile', type_='foreignkey')
    op.drop_constraint(None, 'userprofile', type_='foreignkey')
    op.drop_constraint(None, 'userprofile', type_='foreignkey')
    op.drop_constraint(None, 'userprofile', type_='foreignkey')
    op.create_foreign_key(None, 'userprofile', 'days', ['day_id'], ['id'])
    op.create_foreign_key(None, 'userprofile', 'handicaps', ['handicap_id'], ['id'])
    op.create_foreign_key(None, 'userprofile', 'cities', ['city_id'], ['id'])
    op.create_foreign_key(None, 'userprofile', 'genders', ['gender_id'], ['id'])
    op.create_foreign_key(None, 'userprofile', 'time_of_days', ['time_of_day_id'], ['id'])
    op.create_foreign_key(None, 'userprofile', 'ride_or_walks', ['ride_or_walk_id'], ['id'])
    op.create_foreign_key(None, 'userprofile', 'playing_types', ['playing_type_id'], ['id'])
    op.create_foreign_key(None, 'userprofile', 'smokings', ['smoking_id'], ['id'])
    op.create_foreign_key(None, 'userprofile', 'golf_courses', ['golf_course_id'], ['id'])
    op.create_foreign_key(None, 'userprofile', 'drinkings', ['drinking_id'], ['id'])
    op.create_foreign_key(None, 'userprofile', 'states', ['state_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'userprofile', type_='foreignkey')
    op.drop_constraint(None, 'userprofile', type_='foreignkey')
    op.drop_constraint(None, 'userprofile', type_='foreignkey')
    op.drop_constraint(None, 'userprofile', type_='foreignkey')
    op.drop_constraint(None, 'userprofile', type_='foreignkey')
    op.drop_constraint(None, 'userprofile', type_='foreignkey')
    op.drop_constraint(None, 'userprofile', type_='foreignkey')
    op.drop_constraint(None, 'userprofile', type_='foreignkey')
    op.drop_constraint(None, 'userprofile', type_='foreignkey')
    op.drop_constraint(None, 'userprofile', type_='foreignkey')
    op.drop_constraint(None, 'userprofile', type_='foreignkey')
    op.create_foreign_key(None, 'userprofile', 'golf_course', ['golf_course_id'], ['id'])
    op.create_foreign_key(None, 'userprofile', 'smoking', ['smoking_id'], ['id'])
    op.create_foreign_key(None, 'userprofile', 'state', ['state_id'], ['id'])
    op.create_foreign_key(None, 'userprofile', 'playing_type', ['playing_type_id'], ['id'])
    op.create_foreign_key(None, 'userprofile', 'city', ['city_id'], ['id'])
    op.create_foreign_key(None, 'userprofile', 'handicap', ['handicap_id'], ['id'])
    op.create_foreign_key(None, 'userprofile', 'drinking', ['drinking_id'], ['id'])
    op.create_foreign_key(None, 'userprofile', 'day', ['day_id'], ['id'])
    op.create_foreign_key(None, 'userprofile', 'time_of_day', ['time_of_day_id'], ['id'])
    op.create_foreign_key(None, 'userprofile', 'gender', ['gender_id'], ['id'])
    op.create_foreign_key(None, 'userprofile', 'ride_or_walk', ['ride_or_walk_id'], ['id'])
    op.create_table('drinking',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('drinking', sa.VARCHAR(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('smoking',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('smoking', sa.VARCHAR(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('state',
    sa.Column('id', sa.INTEGER(), nullable=True),
    sa.Column('state_id', sa.VARCHAR(length=64), nullable=False),
    sa.Column('state', sa.VARCHAR(length=64), nullable=True),
    sa.PrimaryKeyConstraint('state_id')
    )
    op.create_table('time_of_day',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('time_of_day', sa.VARCHAR(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('golf_course',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('city', sa.VARCHAR(length=64), nullable=True),
    sa.Column('state', sa.VARCHAR(length=64), nullable=True),
    sa.Column('course', sa.VARCHAR(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('day',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('day', sa.VARCHAR(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('gender',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('gender', sa.VARCHAR(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('handicap',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('handicap', sa.VARCHAR(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('city',
    sa.Column('id', sa.INTEGER(), nullable=True),
    sa.Column('city_id', sa.VARCHAR(length=64), nullable=False),
    sa.Column('city', sa.VARCHAR(length=64), nullable=True),
    sa.PrimaryKeyConstraint('city_id')
    )
    op.create_table('playing_type',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('playing_type', sa.VARCHAR(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ride_or_walk',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('ride_or_walk', sa.VARCHAR(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('time_of_days')
    op.drop_table('states')
    op.drop_table('smokings')
    op.drop_table('ride_or_walks')
    op.drop_table('playing_types')
    op.drop_table('handicaps')
    op.drop_table('golf_courses')
    op.drop_table('genders')
    op.drop_table('drinkings')
    op.drop_table('days')
    op.drop_table('cities')
    # ### end Alembic commands ###