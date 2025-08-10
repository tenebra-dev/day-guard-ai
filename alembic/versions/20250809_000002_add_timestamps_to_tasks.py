"""add timestamps to tasks

Revision ID: 20250809_000002
Revises: 20250809_000001
Create Date: 2025-08-09

"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "20250809_000002"
down_revision = "20250809_000001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Force table recreate on SQLite to support NOT NULL + expression defaults
    with op.batch_alter_table("tasks", recreate="always") as batch_op:
        batch_op.add_column(
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                nullable=False,
                server_default=sa.text("CURRENT_TIMESTAMP"),
            )
        )
        batch_op.add_column(
            sa.Column(
                "updated_at",
                sa.DateTime(timezone=True),
                nullable=False,
                server_default=sa.text("CURRENT_TIMESTAMP"),
            )
        )


def downgrade() -> None:
    with op.batch_alter_table("tasks", recreate="always") as batch_op:
        batch_op.drop_column("updated_at")
        batch_op.drop_column("created_at")
