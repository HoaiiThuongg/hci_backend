"""add users.email (nullable)

Revision ID: c4d8e5f701ab
Revises: 8eecd691f16d
Create Date: 2026-11-05

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'c4d8e5f701ab'
down_revision: Union[str, Sequence[str], None] = '8eecd691f16d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('email', sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'email')
