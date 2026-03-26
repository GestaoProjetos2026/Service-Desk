from typing import Optional
from uuid import UUID

from sqlmodel import Session, select
from sqlalchemy import func

from app.modules.tickets.model import Ticket, TicketStatus
from app.modules.tickets.schema import TicketCreate, TicketUpdate


class TicketRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, data: TicketCreate) -> Ticket:
        ticket = Ticket(**data.model_dump())
        self._session.add(ticket)
        self._session.commit()
        self._session.refresh(ticket)
        return ticket

    def get_by_id(self, ticket_id: UUID) -> Optional[Ticket]:
        return self._session.get(Ticket, ticket_id)

    def list_all(self, skip: int = 0, limit: int = 50) -> tuple[int, list[Ticket]]:
        total = self._session.scalar(select(func.count()).select_from(Ticket))
        result = self._session.exec(
            select(Ticket).order_by(Ticket.created_at.desc()).offset(skip).limit(limit)
        )
        tickets = result.all()
        return total, list(tickets)

    def update(self, ticket: Ticket, data: TicketUpdate) -> Ticket:
        from datetime import datetime

        update_data = data.model_dump(exclude_unset=True)

        # Auto-set closed_at when status transitions to done
        if update_data.get("status") == TicketStatus.done and ticket.status != TicketStatus.done:
            update_data["closed_at"] = datetime.utcnow()

        for field, value in update_data.items():
            setattr(ticket, field, value)

        self._session.add(ticket)
        self._session.commit()
        self._session.refresh(ticket)
        return ticket

    def delete(self, ticket: Ticket) -> None:
        self._session.delete(ticket)
        self._session.commit()
