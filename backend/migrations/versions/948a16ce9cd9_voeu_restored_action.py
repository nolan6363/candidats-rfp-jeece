"""voeu_restored action

Revision ID: 948a16ce9cd9
Revises: d99a5e628d96
Create Date: 2026-03-24 16:08:10.908381

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '948a16ce9cd9'
down_revision = 'd99a5e628d96'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("ALTER TABLE action_logs MODIFY COLUMN IF EXISTS action ENUM('abandoned', 'restored', 'voeu_deleted', 'voeu_restored') NOT NULL")


def downgrade():
    op.execute("ALTER TABLE action_logs MODIFY COLUMN action ENUM('abandoned', 'restored', 'voeu_deleted') NOT NULL")
