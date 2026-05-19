"""add activity calories_burned column

Revision ID: add_activity_calories
Revises: 81adbc2aab2d
Create Date: 2024-05-17 06:45:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_activity_calories'
down_revision = '81adbc2aab2d'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('activity', sa.Column('calories_burned', sa.Integer(), nullable=False, server_default='0'))

def downgrade():
    op.drop_column('activity', 'calories_burned') 