"""add workout timestamp column

Revision ID: add_workout_timestamp
Revises: add_workout_calories
Create Date: 2024-05-17 06:10:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_workout_timestamp'
down_revision = 'add_workout_calories'
branch_labels = None
depends_on = None

def upgrade():
    # Add timestamp column to workout table
    op.add_column('workout', sa.Column('timestamp', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')))

def downgrade():
    # Remove timestamp column from workout table
    op.drop_column('workout', 'timestamp') 