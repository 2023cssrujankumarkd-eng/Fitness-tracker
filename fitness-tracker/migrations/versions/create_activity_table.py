"""create activity table

Revision ID: create_activity_table
Revises: add_workout_timestamp
Create Date: 2024-05-17 06:15:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'create_activity_table'
down_revision = 'add_workout_timestamp'
branch_labels = None
depends_on = None

def upgrade():
    # Create activity table
    op.create_table('activity',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('type', sa.String(length=50), nullable=False),
        sa.Column('duration', sa.Integer(), nullable=False),
        sa.Column('calories_burned', sa.Integer(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    # Drop activity table
    op.drop_table('activity') 