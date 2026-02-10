"""create file shares table

Revision ID: 2ce090d0956e
Revises: 4561f3a967da
Create Date: 2026-02-08 15:30:42.579704
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2ce090d0956e"
down_revision: Union[str, Sequence[str], None] = "4561f3a967da"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "file_shares",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("file_id", sa.UUID(), nullable=False),
        sa.Column("token", sa.UUID(), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["file_id"],
            ["files.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_file_shares_file_id"),
        "file_shares",
        ["file_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_file_shares_token"),
        "file_shares",
        ["token"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_file_shares_token"), table_name="file_shares")
    op.drop_index(op.f("ix_file_shares_file_id"), table_name="file_shares")
    op.drop_table("file_shares")
