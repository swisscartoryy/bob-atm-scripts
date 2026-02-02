# type: ignore
import re
import inflection

from enum import IntEnum
from typing import Annotated
from datetime import datetime

from annotated_doc import Doc
from pydantic import BaseModel, Field, field_validator, computed_field


class PointOfInterestId(IntEnum):
    ATM = 1
    BRANCH = 2
    SELF_SERVICE_TERMINAL = 3
    BRANCH_WITH_EXTENDED_HOURS = 4


class BoliviaStateId(IntEnum):
    BENI: Annotated[int, Doc("Beni state, Bolivia")] = 9
    PANDO: Annotated[int, Doc("Pando state, Bolivia")] = 8
    ORURO: Annotated[int, Doc("Oruro state, Bolivia")] = 6

    LA_PAZ: Annotated[int, Doc("La Paz state, Bolivia")] = 1
    TARIJA: Annotated[int, Doc("Tarija state, Bolivia")] = 5
    POTOSI: Annotated[int, Doc("Potosí state, Bolivia")] = 7

    SANTA_CRUZ: Annotated[int, Doc("Santa Cruz state, Bolivia")] = 2
    COCHABAMBA: Annotated[int, Doc("Cochabamba state, Bolivia")] = 3
    CHUQUISACA: Annotated[int, Doc("Chuquisaca state, Bolivia")] = 4


class BoliviaCityId(IntEnum):
    LA_PAZ: Annotated[int, Doc("La Paz city, La Paz")] = 1
    EL_ALTO: Annotated[int, Doc("El Alto city, La Paz")] = 3

    ORURO: Annotated[int, Doc("Oruro city, Oruro")] = 15
    SUCRE: Annotated[int, Doc("Sucre city, Chuquisaca")] = 11

    COBIJA: Annotated[int, Doc("Cobija city, Pando")] = 17
    POTOSI: Annotated[int, Doc("Potosí city, Potosí")] = 16
    TRINIDAD: Annotated[int, Doc("Trinidad city, Beni")] = 18

    TARIJA: Annotated[int, Doc("Tarija city, Tarija")] = 12
    YACUIBA: Annotated[int, Doc("Yacuiba city, Tarija")] = 14
    VILLAMONTES: Annotated[int, Doc("Villamontes city, Tarija")] = 13

    COCHABAMBA: Annotated[int, Doc("Cochabamba city, Cochabamba")] = 9
    QUILLA_COLLO: Annotated[int, Doc("Quillacollo city, Cochabamba")] = 10

    CAMIRI: Annotated[int, Doc("Camiri city, Santa Cruz")] = 8
    MONTERO: Annotated[int, Doc("Montero city, Santa Cruz")] = 5
    SANTA_CRUZ: Annotated[int, Doc("Santa Cruz city, Santa Cruz")] = 4
    PUERTO_SUAREZ: Annotated[int, Doc("Puerto Suárez city, Santa Cruz")] = 6
    ARROYO_CONCEPCION: Annotated[int, Doc("Arroyo Concepción city, Santa Cruz")] = 7


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

    email: Annotated[str, Doc("contact email")]
    telephone: Annotated[str, Doc("contact phonenumber")]

    type: Annotated[PointOfInterest, Doc("type PoI")] = Field(exclude=True)
    working_hours: Annotated[str, Doc("opening hours / availability")] = Field(
        validation_alias="workingHours"
    )

    @computed_field
    @property
    def poitype(self) -> Annotated[str, Doc("normalized PoI")]:
        return inflection.underscore(self.type.value_name).upper()

    city: Annotated[BoliviaCity | None, Doc("branch / ATM city")] = Field(
        exclude=True,
        default=None,
    )

    @computed_field(alias="cityName")
    @property
    def city_name(self) -> Annotated[str | None, Doc("branch / ATM city")]:
        return (
            None if self.city is None else re.sub(r"\s+", "_", self.city.name.upper())
        )

    state: Annotated[BoliviaState | None, Doc("branch / ATM state")] = Field(
        default=None,
        exclude=True,
    )

    @computed_field(alias="stateName")
    @property
    def state_name(self) -> Annotated[str | None, Doc("branch / ATM state")]:
        return (
            None if self.state is None else re.sub(r"\s+", "_", self.state.name.upper())
        )

    is_deleted: bool = Field(validation_alias="isDeleted", exclude=True)
    creation_date: datetime = Field(validation_alias="creationDate", exclude=True)
    modified_date: datetime = Field(validation_alias="modifiedDate", exclude=True)

    @field_validator("*", mode="before")
    def normalize_string(string):
        return (
            string
            if not isinstance(string, str)
            else re.sub(r"\s+", " ", string.strip())
        )
