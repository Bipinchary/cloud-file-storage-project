"""add_file_status_fixed

Revision ID: dd30903605d0
Revises: 2ce090d0956e
Create Date: 2026-02-10 21:49:29.054639

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd30903605d0'
down_revision: Union[str, Sequence[str], None] = '2ce090d0956e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create the PostgreSQL ENUM type
    # Using 'execute' because Postgres needs the type to exist before the column
    op.execute("CREATE TYPE file_status AS ENUM ('PENDING', 'ACTIVE', 'FAILED')")

    # 2. Add the column to the 'files' table
    op.add_column('files', 
        sa.Column('status', 
                  sa.Enum('PENDING', 'ACTIVE', 'FAILED', name='file_status'), 
                  nullable=False, 
                  server_default='PENDING')
    )


def downgrade() -> None:
    # 1. Remove the column
    op.drop_column('files', 'status')

    # 2. Remove the ENUM type
    op.execute("DROP TYPE file_status")
