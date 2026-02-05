import re

from annotated_doc import Doc

from typing import Annotated, Optional
from pydantic import BaseModel, Field, computed_field, model_validator, field_validator

from .enums import BnbTipoEntidadId, BnbSubtipoEntidadId, BnbDepartamentoId


class BnbDepartamentoRoot(BaseModel):
    id: BnbDepartamentoId = Field(validation_alias="ID")

    departamento: Annotated[str, Doc("nombre departamento")] = Field(
        validation_alias="Departamento",
    )

    detalles: Annotated[list[BnbBranchATM], Doc("Branch / ATM list")] = Field(
        validation_alias="Detalles",
    )

    @model_validator(mode="after")
    def asignar_departamento(self) -> BnbDepartamentoRoot:
        for branchatm in self.detalles:
            branchatm.departamentoid = self.id

        return self


class BnbBranchATM(BaseModel):
    id: int = Field(validation_alias="Codigo")

    tipopoi: Annotated[BnbTipoEntidadId, Doc("Branch / ATM")] = Field(
        exclude=True,
        validation_alias="Tipo",
    )

    @computed_field
    def tipo(self) -> Annotated[str, Doc("Branch / ATM")]:
        return BnbTipoEntidadId(self.tipopoi).name

    subtipopoi: Annotated[BnbSubtipoEntidadId, Doc("subtipo Branch / ATM")] = Field(
        exclude=True,
        validation_alias="SubTipo",
    )

    @computed_field
    def subtipo(self) -> Annotated[str, Doc("subtipo Branch / ATM")]:
        return BnbSubtipoEntidadId(self.subtipopoi).name

    tipo_nombre: Optional[str] = Field(
        default=None,
        exclude=True,
        validation_alias="TipoNombre",
    )

    descripcion: str = Field(validation_alias="Descripcion")

    latitud: float = Field(validation_alias="Latitud")
    longitud: float = Field(validation_alias="Longitud")

    horarios: str = Field(validation_alias="Horarios")
    direccion: str = Field(validation_alias="Direccion")

    fax: str = Field(validation_alias="Fax")
    billetaje: str = Field(validation_alias="Billetaje", exclude=True)
    promocion: str = Field(validation_alias="Promocion", exclude=True)

    interno1: str = Field(validation_alias="Interno1", exclude=True)
    interno2: str = Field(validation_alias="Interno2", exclude=True)

    telefono1: str = Field(validation_alias="Telefono1", exclude=True)
    telefono2: str = Field(validation_alias="Telefono2", exclude=True)

    @computed_field
    def telefonos(self) -> str:
        telefono2 = f", {self.telefono2}" if len(self.telefono2) > 0 else ""
        return f"{self.telefono1}{telefono2}"

    departamentoid: Optional[BnbDepartamentoId] = Field(
        default=None,
        exclude=True,
    )

    @computed_field
    def departamento(self) -> Optional[str]:
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
