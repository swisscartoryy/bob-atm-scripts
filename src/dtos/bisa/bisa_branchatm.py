# type: ignore
import re
import inflection

from datetime import datetime
from annotated_doc import Doc

from typing import Optional, Annotated
from pydantic import BaseModel, Field, field_validator, computed_field

from .enums import BoliviaCityId, BoliviaStateId, PointOfInterestId


class BoliviaCity(BaseModel):
    city_id: BoliviaCityId = Field(validation_alias="cityId")
    name: str


class BoliviaState(BaseModel):
    state_id: BoliviaStateId = Field(validation_alias="stateId")
    name: str


class PointOfInterest(BaseModel):
    value: Annotated[PointOfInterestId, Doc("PoI type")]
    value_name: Annotated[str, Doc("PoI name")] = Field(
        validation_alias="valueName",
    )

    is_enum: bool = Field(validation_alias="isEnum")
    type: Annotated[str, Doc("backend internal type namespace")] = Field(
        validation_alias="$type"
    )


class BisaBranchATM(BaseModel):
    id: int
    name: str

    latitude: float
    longitude: float

    address: Annotated[str, Doc("location address")]
    notes: Annotated[str, Doc("additional notes / comments")]

    email: Annotated[str, Doc("contact email")] = Field(exclude=True)
    telephone: Annotated[str, Doc("contact phonenumber")]

    typepoi: Annotated[PointOfInterest, Doc("type PoI")] = Field(
        exclude=True,
        validation_alias="type",
    )

    working_hours: Annotated[str, Doc("opening hours / availability")] = Field(
        validation_alias="workingHours",
    )

    @computed_field(alias="typecol")
    def type(self) -> Annotated[str, Doc("normalized PoI")]:
        return inflection.underscore(self.typepoi.value_name).upper()

    statecity: Annotated[Optional[BoliviaCity], Doc("branch / ATM city")] = Field(
        default=None,
        exclude=True,
        validation_alias="city",
    )

    @computed_field
    def city(self) -> Annotated[Optional[str], Doc("branch / ATM city")]:
        return (
            None
            if self.statecity is None
            else re.sub(r"\s+", "_", self.statecity.name.upper())
        )

    state: Annotated[Optional[BoliviaState], Doc("branch / ATM state")] = Field(
        default=None,
        exclude=True,
    )

    @computed_field
    def department(self) -> Annotated[Optional[str], Doc("branch / ATM state")]:
        return (
            None if self.state is None else re.sub(r"\s+", "_", self.state.name.upper())
        )

    isdeleted: bool = Field(validation_alias="isDeleted", exclude=True)
    creation_date: datetime = Field(validation_alias="creationDate", exclude=True)
    modified_date: datetime = Field(validation_alias="modifiedDate", exclude=True)

    @field_validator("*", mode="before")
    def strip_props(string):
        return (
            string
            if not isinstance(string, str)
            else re.sub(r"\s+", " ", string.strip())
        )
