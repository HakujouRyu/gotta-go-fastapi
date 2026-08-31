"""Add items table

Revision ID: 3199f8b81ea9
Revises:
Create Date: 2026-09-01 08:18:17.218709

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "3199f8b81ea9"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "items",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("items")
