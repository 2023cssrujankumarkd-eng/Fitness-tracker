"""merge heads

Revision ID: 81adbc2aab2d
Revises: add_activity_columns, add_workout_notes
Create Date: 2025-05-17 06:17:33.132728

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81adbc2aab2d'
down_revision = ('add_activity_columns', 'add_workout_notes')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
