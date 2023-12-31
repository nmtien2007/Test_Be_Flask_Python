"""empty message

Revision ID: 8966873448fc
Revises: 0eb3ccc1b53e
Create Date: 2023-12-28 21:17:43.439451

"""
from alembic import op
import sqlalchemy as sa

import sqlalchemy_utils

# revision identifiers, used by Alembic.
revision = '8966873448fc'
down_revision = '0eb3ccc1b53e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_score',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('scores', sqlalchemy_utils.types.json.JSONType(), nullable=False),
    sa.Column('high_subjects', sqlalchemy_utils.types.scalar_list.ScalarListType(), nullable=False),
    sa.Column('avg_score', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_unique_constraint(None, 'users', ['email'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_table('user_score')
    # ### end Alembic commands ###
