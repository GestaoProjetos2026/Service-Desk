"""Add tickets and ticket_messages tables

Revision ID: 0001
Revises: 
Create Date: 2026-03-25 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'tickets',
        sa.Column('id', sa.CHAR(length=36), primary_key=True, nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('status', sa.Enum('pending', 'in_process', 'done', 'canceled', name='ticketstatus'), nullable=False, server_default='pending'),
        sa.Column('priority', sa.Enum('low', 'normal', 'high', 'urgent', name='ticketpriority'), nullable=False, server_default='normal'),
        sa.Column('user_id', sa.CHAR(length=36), nullable=True),
        sa.Column('client_id', sa.CHAR(length=36), nullable=True),
        sa.Column('assigned_to', sa.CHAR(length=36), nullable=True),
        sa.Column('updated_by', sa.CHAR(length=36), nullable=True),
        sa.Column('category', sa.String(length=100), nullable=True),
        sa.Column('closed_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
    )

    op.create_table(
        'ticket_messages',
        sa.Column('id', sa.CHAR(length=36), primary_key=True, nullable=False),
        sa.Column('ticket_id', sa.CHAR(length=36), nullable=False),
        sa.Column('author_id', sa.CHAR(length=36), nullable=True),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('is_internal', sa.Boolean(), nullable=False, server_default=sa.text('0')),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['ticket_id'], ['tickets.id'], ondelete='CASCADE', name='fk_tm_ticket'),
    )


def downgrade() -> None:
    op.drop_table('ticket_messages')
    op.drop_table('tickets')
    sa.Enum(name='ticketstatus').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='ticketpriority').drop(op.get_bind(), checkfirst=True)
