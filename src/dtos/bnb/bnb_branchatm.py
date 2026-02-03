import re

from annotated_doc import Doc

from typing import Annotated, Optional
from pydantic import BaseModel, Field, computed_field, model_validator, field_validator

from .enums import BnbTipoEntidadId, BnbSubtipoEntidadId, BnbDepartamentoId


class BnbDepartamento(BaseModel):
    id: BnbDepartamentoId = Field(validation_alias="ID")

    departamento: Annotated[str, Doc("nombre departamento")] = Field(
        validation_alias="Departamento",
    )

    detalles: Annotated[list[BnbBranchATM], Doc("Branch / ATM list")] = Field(
        validation_alias="Detalles",
    )

    @model_validator(mode="after")
    def asignar_departamento(self) -> BnbDepartamento:
        for branchatm in self.detalles:
            branchatm.departamentoid = self.id

        return self


class BnbBranchATM(BaseModel):
    model_config = {
        "populate_by_name": True,
    }

    codigo: int = Field(validation_alias="Codigo")

    tipo: Annotated[int, Doc("Branch / ATM")] = Field(
        exclude=True,
        validation_alias="Tipo",
    )

    @computed_field(alias="tipoEntidad")
    @property
    def tipo_entidad(self) -> Annotated[str, Doc("Branch / ATM")]:
        return BnbTipoEntidadId(self.tipo).name

    subtipo: Annotated[int, Doc("subtipo Branch / ATM")] = Field(
        exclude=True,
        validation_alias="SubTipo",
    )

    @computed_field(alias="subtipoEntidad")
    @property
    def subtipo_entidad(self) -> Annotated[str, Doc("subtipo Branch / ATM")]:
        return BnbSubtipoEntidadId(self.subtipo).name

    tipo_nombre: Optional[str] = Field(
        default=None,
        validation_alias="TipoNombre",
    )

    descripcion: str = Field(validation_alias="Descripcion")

    latitud: float = Field(validation_alias="Latitud")
    longitud: float = Field(validation_alias="Longitud")

    horarios: str = Field(validation_alias="Horarios")
    direccion: str = Field(validation_alias="Direccion")

    fax: str = Field(validation_alias="Fax")
    billetaje: str = Field(validation_alias="Billetaje")
    promocion: str = Field(validation_alias="Promocion")

    interno1: str = Field(validation_alias="Interno1")
    interno2: str = Field(validation_alias="Interno2")

    telefono1: str = Field(validation_alias="Telefono1")
    telefono2: str = Field(validation_alias="Telefono2")

    departamentoid: Optional[int] = Field(
        default=None,
        exclude=True,
    )

    @computed_field(alias="nombreDepartamento")
    @property
    def nombre_departamento(self) -> Optional[str]:
        return (
            None
            if self.departamentoid is None
            else BnbDepartamentoId(self.departamentoid).name
        )

    @field_validator("*", mode="before")
    def strip_props(cls, prop_value):
        return (
            prop_value
            if not isinstance(prop_value, str)
            else re.sub(r"\s+", " ", prop_value).strip()
        )
