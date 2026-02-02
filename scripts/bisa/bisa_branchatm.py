# type: ignore
import re
import inflection

from enum import IntEnum
from typing import Annotated
from datetime import datetime

from annotated_doc import Doc
from pydantic import BaseModel, Field, field_validator, computed_field


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


class StateId(IntEnum):
    BENI: Annotated[int, Doc("Departamento del Beni, Bolivia")] = 9
    PANDO: Annotated[int, Doc("Departamento de Pando, Bolivia")] = 8
    ORURO: Annotated[int, Doc("Departamento de Oruro, Bolivia")] = 6

    LA_PAZ: Annotated[int, Doc("Departamento de La Paz, Bolivia")] = 1
    TARIJA: Annotated[int, Doc("Departamento de Tarija, Bolivia")] = 5
    POTOSI: Annotated[int, Doc("Departamento de Potosí, Bolivia")] = 7

    SANTA_CRUZ: Annotated[int, Doc("Departamento de Santa Cruz, Bolivia")] = 2
    COCHABAMBA: Annotated[int, Doc("Departamento de Cochabamba, Bolivia")] = 3
    CHUQUISACA: Annotated[int, Doc("Departamento de Chuquisaca, Bolivia")] = 4


class CityId(IntEnum):
    LA_PAZ: Annotated[int, Doc("Ciudad de La Paz, Dep. La Paz")] = 1
    EL_ALTO: Annotated[int, Doc("Ciudad de El Alto, Dep. La Paz")] = 3

    ORURO: Annotated[int, Doc("Ciudad de Oruro, Dep. Oruro")] = 15
    SUCRE: Annotated[int, Doc("Ciudad de Sucre, Dep. Chuquisaca")] = 11

    COBIJA: Annotated[int, Doc("Ciudad de Cobija, Dep. Pando")] = 17
    POTOSI: Annotated[int, Doc("Ciudad de Potosí, Dep. Potosí")] = 16
    TRINIDAD: Annotated[int, Doc("Ciudad de Trinidad, Dep. Beni")] = 18

    TARIJA: Annotated[int, Doc("Ciudad de Tarija, Dep. Tarija")] = 12
    YACUIBA: Annotated[int, Doc("Ciudad de Yacuiba, Dep. Tarija")] = 14
    VILLAMONTES: Annotated[int, Doc("Ciudad de Villamontes, Dep. Tarija")] = 13

    COCHABAMBA: Annotated[int, Doc("Ciudad de Cochabamba, Dep. Cochabamba")] = 9
    QUILLA_COLLO: Annotated[int, Doc("Ciudad de Quillacollo, Dep. Cochabamba")] = 10

    CAMIRI: Annotated[int, Doc("Ciudad de Camiri, Dep. Santa Cruz")] = 8
    MONTERO: Annotated[int, Doc("Ciudad de Montero, Dep. Santa Cruz")] = 5
    SANTA_CRUZ: Annotated[int, Doc("Ciudad de Santa Cruz, Dep. Santa Cruz")] = 4
    PUERTO_SUAREZ: Annotated[int, Doc("Ciudad de Puerto Suárez, Dep. Santa Cruz")] = 6
    ARROYO_CONCEPCION: Annotated[
        int, Doc("Ciudad de Arroyo Concepción, Dep. Santa Cruz")
    ] = 7


class City(BaseModel):
    model_config = {
        "populate_by_name": True,
    }

    city_id: Annotated[CityId, Doc("Identificador único de la ciudad")] = Field(
        alias="cityId"
    )

    name: Annotated[str, Doc("Nombre de la ciudad")]


class State(BaseModel):
    model_config = {
        "populate_by_name": True,
    }

    state_id: Annotated[
        StateId, Doc("Identificador único del departamento o estado")
    ] = Field(alias="stateId")

    name: Annotated[str, Doc("Nombre del departamento o estado")]


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

    latitude: Annotated[float, Doc("Latitud geográfica en formato decimal")]
    longitude: Annotated[float, Doc("Longitud geográfica en formato decimal")]

    address: Annotated[str, Doc("Dirección física completa")]
    notes: Annotated[str, Doc("Notas adicionales o comentarios")]

    email: Annotated[str, Doc("Correo electrónico de contacto")]
    telephone: Annotated[str, Doc("Número telefónico de contacto")]

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
    ] = Field(alias="isDeleted", exclude=True)

    working_hours: Annotated[str, Doc("Horario de atención o disponibilidad")] = Field(
        alias="workingHours"
    )

    city: Annotated[
        City | None,
        Doc("Ciudad donde se encuentra la sucursal/ATM"),
    ] = Field(default=None, exclude=True)

    @computed_field(alias="cityName")
    @property
    def city_name(self) -> Annotated[
        str | None,
        Doc("Ciudad donde se encuentra la sucursal/ATM"),
    ]:
        return (
            None if self.city is None else re.sub(r"\s+", "_", self.city.name.upper())
        )

    state: Annotated[
        State | None,
        Doc("Departamento donde se encuentra la sucursal/ATM"),
    ] = Field(default=None, exclude=True)

    @computed_field(alias="stateName")
    @property
    def state_name(self) -> Annotated[
        str | None,
        Doc("Departamento donde se encuentra la sucursal/ATM"),
    ]:
        return (
            None if self.state is None else re.sub(r"\s+", "_", self.state.name.upper())
        )

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
