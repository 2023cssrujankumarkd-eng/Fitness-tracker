"""add workout duration column

Revision ID: add_workout_duration
Revises: add_workout_type
Create Date: 2024-05-17 06:01:54.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_workout_duration'
down_revision = 'add_workout_type'
branch_labels = None
depends_on = None

def upgrade():
    # Add duration column to workout table
    op.add_column('workout', sa.Column('duration', sa.Integer(), nullable=False, server_default='30'))

def downgrade():
    # Remove duration column from workout table
    op.drop_column('workout', 'duration') 