from typing import Optional
from pydantic import BaseModel


class BankServicePoint(BaseModel):
    id: str
    bankcode: str

    type: str
    subtype: Optional[str]

    name: str
    description: Optional[str]

    city: Optional[str]
    address: Optional[str]
    department: Optional[str]

    latitude: float
    longitude: float

    phonenumber: str
    opening_hours: Optional[str]
    additional_info: Optional[str]
