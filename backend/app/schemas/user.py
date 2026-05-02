from pydantic import BaseModel
from pydantic import ConfigDict


class UserCreate(BaseModel):
    full_name: str
    phone: str
    password: str
    language: str = "en"


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    phone: str
    language: str
    is_admin: bool
