"""Initial schema

Revision ID: 001_initial
Revises: 
Create Date: 2026-03-29 01:21:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'transactions',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('description', sa.String(length=200), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('transaction_type', sa.String(length=10), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False, server_default='uncategorized'),
        sa.Column('auto_tagged', sa.Boolean(), server_default='1'),
        sa.Column('status', sa.String(length=20), server_default='pending'),
        sa.Column('timestamp', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('status_changed_at', sa.DateTime(), nullable=True),
        sa.Column('status_changed_by', sa.String(length=100), nullable=True),
        sa.Column('is_duplicate', sa.Boolean(), server_default='0'),
        sa.Column('duplicate_of', sa.Integer(), nullable=True),
    )
    
    op.create_index('idx_timestamp', 'transactions', ['timestamp'])
    op.create_index('idx_category_timestamp', 'transactions', ['category', 'timestamp'])
    op.create_index('idx_duplicate_check', 'transactions', ['description', 'amount', 'timestamp'])
    op.create_index('idx_status', 'transactions', ['status'])
    op.create_index('idx_type_category_month', 'transactions', ['transaction_type', 'category', 'timestamp'])
    op.create_index('idx_created_at', 'transactions', ['created_at'])


def downgrade() -> None:
    op.drop_table('transactions')
