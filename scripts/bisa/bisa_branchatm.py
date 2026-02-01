# type: ignore
import re
import inflection

from enum import IntEnum
from typing import Annotated
from datetime import datetime

from annotated_doc import Doc
from pydantic import BaseModel, Field, field_validator, computed_field


class CityId(IntEnum):
    SUCRE: Annotated[int, Doc("Ciudad: Sucre")] = 11
    ORURO: Annotated[int, Doc("Ciudad: Oruro")] = 15
    LA_PAZ: Annotated[int, Doc("Ciudad: La Paz")] = 1
    COBIJA: Annotated[int, Doc("Ciudad: Cobija")] = 17
    POTOSI: Annotated[int, Doc("Ciudad: Potosí")] = 16
    TARIJA: Annotated[int, Doc("Ciudad: Tarija")] = 12
    TRINIDAD: Annotated[int, Doc("Ciudad: Trinidad")] = 18
    COCHABAMBA: Annotated[int, Doc("Ciudad: Cochabamba")] = 9
    SANTA_CRUZ: Annotated[int, Doc("Ciudad: Santa Cruz")] = 4


class City(BaseModel):
    model_config = {
        "populate_by_name": True,
    }

    city_id: Annotated[int, Doc("Identificador único de la ciudad")] = Field(
        alias="cityId"
    )

    name: Annotated[str, Doc("Nombre de la ciudad")]


class State(BaseModel):
    model_config = {
        "populate_by_name": True,
    }

    state_id: Annotated[int, Doc("Identificador único del departamento o estado")] = (
        Field(alias="stateId")
    )

    name: Annotated[str, Doc("Nombre del departamento o estado")]


class PointOfInterestId(IntEnum):
    ATM: Annotated[int, Doc("Cajero automático (ATM)")] = 1
    BRANCH: Annotated[int, Doc("Sucursal bancaria tradicional")] = 2

    SELF_SERVICE_TERMINAL: Annotated[
        int,
        Doc("Terminal de autoservicio dentro o fuera de sucursal"),
    ] = 3

    BRANCH_WITH_EXTENDED_HOURS: Annotated[
        int, Doc("Sucursal con horario extendido o corresponsal bancario")
    ] = 4


class PointOfInterest(BaseModel):
    model_config = {
        "populate_by_name": True,
    }

    value: Annotated[
        PointOfInterestId,
        Doc("Valor numérico que representa el tipo de punto de interés"),
    ]

    value_name: Annotated[
        str, Doc("Nombre descriptivo del tipo de punto de interés")
    ] = Field(alias="valueName")

    type: Annotated[
        str, Doc("Tipo interno totalmente calificado (namespace del backend)")
    ] = Field(alias="$type")

    is_enum: Annotated[bool, Doc("Indica si el tipo corresponde a un Enum")] = Field(
        alias="isEnum"
    )


class BisaBranchATM(BaseModel):
    model_config = {
        "populate_by_name": True,
    }

    id: Annotated[int, Doc("Identificador único interno de la sucursal o ATM")]
    name: Annotated[str, Doc("Nombre comercial de la sucursal o ATM")]

    notes: Annotated[str, Doc("Notas adicionales o comentarios")]
    address: Annotated[str, Doc("Dirección física completa")]

    telephone: Annotated[str, Doc("Número telefónico de contacto")]
    email: Annotated[str, Doc("Correo electrónico de contacto")]

    type: Annotated[
        PointOfInterest, Doc("Tipo de punto de interés (Sucursal, ATM, etc.)")
    ] = Field(exclude=True)

    @computed_field
    @property
    def poitype(self) -> Annotated[
        str,
        Doc("Tipo de punto de interés normalizado"),
    ]:
        return inflection.underscore(self.type.value_name).upper()

    is_deleted: Annotated[
        bool, Doc("Indica si el registro se encuentra marcado como eliminado")
    ] = Field(alias="isDeleted")

    working_hours: Annotated[str, Doc("Horario de atención o disponibilidad")] = Field(
        alias="workingHours"
    )

    city: Annotated[
        City | None,
        Doc("Ciudad donde se encuentra la sucursal o ATM"),
    ] = Field(default=None, exclude=True)

    @computed_field
    @property
    def city_name(self) -> Annotated[
        str | None,
        Doc("Ciudad donde se encuentra la sucursal o ATM"),
    ]:
        return (
            None
            if self.city is None
            else re.sub(r"\s+", "_", self.city.name.strip()).upper()
        )

    state: Annotated[
        State | None,
        Doc("Departamento o estado donde se encuentra la sucursal o ATM"),
    ] = Field(default=None)

    latitude: Annotated[float, Doc("Latitud geográfica en formato decimal")]
    longitude: Annotated[float, Doc("Longitud geográfica en formato decimal")]

    creation_date: Annotated[datetime, Doc("Fecha y hora de creación del registro")] = (
        Field(alias="creationDate")
    )

    modified_date: Annotated[
        datetime, Doc("Fecha y hora de la última modificación del registro")
    ] = Field(alias="modifiedDate")

    @field_validator("*", mode="before")
    def normalize_string(string):
        return (
            string
            if not isinstance(string, str)
            else re.sub(r"\s+", " ", string.strip())
        )
