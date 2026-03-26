from typing import Optional
from sqlmodel import SQLModel, Field
from uuid import uuid4

class Ticket(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid4()), primary_key=True, max_length=36)
    title: str = Field(max_length=255)

print(Ticket.schema())
