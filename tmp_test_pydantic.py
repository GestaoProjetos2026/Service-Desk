from pydantic import BaseModel, Field
from uuid import uuid4

class T(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))

print(T.model_json_schema())
