from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import and_, func
from sqlmodel import Session, select

from app.config.database import get_session
from app.modules.tickets.model import Ticket, TicketStatus
from app.modules.tickets.repository import TicketRepository
from app.modules.tickets.schema import (
    TicketCreate,
    TicketListResponse,
    TicketResponse,
    TicketUpdate,
)

router = APIRouter(prefix="/tickets", tags=["Tickets"])


@router.post("", response_model=TicketResponse, status_code=201)
def create_ticket(
    ticket_data: TicketCreate,
    session: Session = Depends(get_session),
) -> TicketResponse:
    repository = TicketRepository(session)
    ticket = repository.create(ticket_data)
    return TicketResponse.model_validate(ticket)


@router.get("", response_model=TicketListResponse, status_code=200)
def list_tickets(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status: Optional[TicketStatus] = Query(None),
    priority: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None),
    client_id: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    session: Session = Depends(get_session),
) -> TicketListResponse:
    repository = TicketRepository(session)
    
    # Build filter conditions
    filters = []
    if status:
        filters.append(Ticket.status == status)
    if priority:
        filters.append(Ticket.priority == priority)
    if user_id:
        filters.append(Ticket.user_id == user_id)
    if client_id:
        filters.append(Ticket.client_id == client_id)
    if category:
        filters.append(Ticket.category == category)
    
    # Execute query with filters
    query = select(Ticket)
    if filters:
        query = query.where(and_(*filters))
    
    query = query.order_by(Ticket.created_at.desc()).offset(skip).limit(limit)
    
    result = session.exec(query)
    tickets = result.all()
    
    # Count total with same filters
    count_query = select(func.count(Ticket.id))
    if filters:
        count_query = count_query.where(and_(*filters))
    
    total_result = session.exec(count_query)
    total = total_result.one() or 0
    
    return TicketListResponse(
        total=int(total),
        items=[TicketResponse.model_validate(ticket) for ticket in tickets],
    )


@router.patch("/{ticket_id}", response_model=TicketResponse, status_code=200)
def update_ticket(
    ticket_id: str,
    ticket_data: TicketUpdate,
    session: Session = Depends(get_session),
) -> TicketResponse:
    repository = TicketRepository(session)
    ticket = repository.get_by_id(ticket_id)
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    updated_ticket = repository.update(ticket, ticket_data)
    return TicketResponse.model_validate(updated_ticket)


@router.post("/{ticket_id}/close", response_model=TicketResponse, status_code=200)
def close_ticket(
    ticket_id: str,
    close_data: TicketUpdate,
    session: Session = Depends(get_session),
) -> TicketResponse:
    repository = TicketRepository(session)
    ticket = repository.get_by_id(ticket_id)
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    if ticket.status == TicketStatus.done:
        raise HTTPException(status_code=400, detail="Ticket is already closed")
    
    close_data.status = TicketStatus.done
    
    updated_ticket = repository.update(ticket, close_data)
    return TicketResponse.model_validate(updated_ticket)


@router.get("/{ticket_id}", response_model=TicketResponse, status_code=200)
def get_ticket(
    ticket_id: str,
    session: Session = Depends(get_session),
) -> TicketResponse:
    repository = TicketRepository(session)
    ticket = repository.get_by_id(ticket_id)
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    return TicketResponse.model_validate(ticket)
