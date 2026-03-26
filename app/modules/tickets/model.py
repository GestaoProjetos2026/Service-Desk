from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import CHAR, Column, ForeignKey
from sqlmodel import Field, SQLModel


class TicketStatus(str, Enum):
    pending = "pending"
    in_process = "in_process"
    done = "done"
    canceled = "canceled"


class TicketPriority(str, Enum):
    low = "low"
    normal = "normal"
    high = "high"
    urgent = "urgent"


def _uuid_pk_column():
    return Column(CHAR(36), primary_key=True, nullable=False)


def _uuid_fk_column(target: str):
    return Column(CHAR(36), ForeignKey(target, ondelete="CASCADE"), nullable=False)


class Ticket(SQLModel, table=True):
    __tablename__ = "tickets"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True, sa_column=_uuid_pk_column())
    title: str = Field(max_length=255, nullable=False)
    description: str = Field(nullable=False)
    status: TicketStatus = Field(default=TicketStatus.pending, nullable=False)
    priority: TicketPriority = Field(default=TicketPriority.normal, nullable=False)
    user_id: Optional[UUID] = Field(default=None, sa_column=Column(CHAR(36), nullable=True), index=True)
    client_id: Optional[UUID] = Field(default=None, sa_column=Column(CHAR(36), nullable=True), index=True)
    assigned_to: Optional[UUID] = Field(default=None, sa_column=Column(CHAR(36), nullable=True), index=True)
    updated_by: Optional[UUID] = Field(default=None, sa_column=Column(CHAR(36), nullable=True), index=True)
    category: Optional[str] = Field(default=None, max_length=100)
    closed_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_column_kwargs={"onupdate": datetime.utcnow},
    )


class TicketMessage(SQLModel, table=True):
    __tablename__ = "ticket_messages"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True, sa_column=_uuid_pk_column())
    ticket_id: UUID = Field(foreign_key="tickets.id", sa_column=_uuid_fk_column("tickets.id"), nullable=False, index=True)
    author_id: Optional[UUID] = Field(default=None, sa_column=Column(CHAR(36), nullable=True), index=True)
    message: str = Field(nullable=False)
    is_internal: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_column_kwargs={"onupdate": datetime.utcnow},
    )
