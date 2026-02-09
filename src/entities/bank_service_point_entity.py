# type: ignore
from typing import Optional
from sqlmodel import SQLModel, Field


class BankServicePointEntity(SQLModel, table=True):
    __tablename__ = "bank_location"

    id: Optional[int] = Field(None, primary_key=True)

    bankid: str = Field(index=True)
    bankcode: str = Field(index=True)

    type: str = Field(index=True)
    subtype: Optional[str] = Field(None)

    name: str
    description: Optional[str] = Field(None)

    city: Optional[str] = Field(None)
    address: Optional[str] = Field(None)
    department: Optional[str] = Field(None)

    latitude: float
    longitude: float

    phonenumber: str
    opening_hours: Optional[str] = Field(None)
    additional_info: Optional[str] = Field(None)
