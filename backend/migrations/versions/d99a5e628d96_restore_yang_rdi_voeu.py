"""restore Yang RDI voeu

Revision ID: d99a5e628d96
Revises: c07528acbd30
Create Date: 2026-03-24 16:03:43.054342

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd99a5e628d96'
down_revision = 'c07528acbd30'
branch_labels = None
depends_on = None


def upgrade():
    # Alexandre Yang (id=53) : restauration du vœu 2 (RDI), supprimé pendant les tests
    op.execute(
        "INSERT IGNORE INTO voeux (candidate_id, rank, role) VALUES (53, 2, 'RDI')"
    )


def downgrade():
    op.execute(
        "DELETE FROM voeux WHERE candidate_id = 53 AND rank = 2 AND role = 'RDI'"
    )
