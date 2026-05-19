"""add workout calories_burned column

Revision ID: add_workout_calories
Revises: add_workout_duration
Create Date: 2024-05-17 06:01:54.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_workout_calories'
down_revision = 'add_workout_duration'
branch_labels = None
depends_on = None

def upgrade():
    # Add calories_burned column to workout table
    op.add_column('workout', sa.Column('calories_burned', sa.Integer(), nullable=False, server_default='0'))

def downgrade():
    # Remove calories_burned column from workout table
    op.drop_column('workout', 'calories_burned') 