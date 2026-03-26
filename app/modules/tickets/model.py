from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4

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


class Ticket(SQLModel, table=True):
    __tablename__ = "tickets"

    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True, max_length=36)
    title: str = Field(max_length=255)
    description: str
    status: TicketStatus = Field(default=TicketStatus.pending)
    priority: TicketPriority = Field(default=TicketPriority.normal)
    user_id: Optional[str] = Field(default=None, max_length=36, index=True)
    client_id: Optional[str] = Field(default=None, max_length=36, index=True)
    assigned_to: Optional[str] = Field(default=None, max_length=36, index=True)
    updated_by: Optional[str] = Field(default=None, max_length=36, index=True)
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

    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True, max_length=36)
    ticket_id: str = Field(foreign_key="tickets.id", max_length=36, index=True)
    author_id: Optional[str] = Field(default=None, max_length=36, index=True)
    message: str
    is_internal: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow},
    )
