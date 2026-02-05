# type: ignore
import re

from annotated_doc import Doc

from typing import Annotated, Optional
from pydantic import BaseModel, field_validator, Field, computed_field

from .enums import TipoBranchATM, SubTipoBranchATM, HorarioAtencion


class GanaBranchATM(BaseModel):
    id: int = Field(validation_alias="ID")

    nombre: str = Field(validation_alias="NOMBRE")
    descripcion: str = Field(validation_alias="DESCRIPCION")

    telefono: Annotated[str, Doc("contact phonenumber")] = Field(
        validation_alias="TELEFONO"
    )

    tipo: Annotated[TipoBranchATM, Doc("branch / ATM")] = Field(
        exclude=True,
        validation_alias="TIPO",
    )

    @computed_field(alias="tipoCol")
    def tipocol(self) -> str:
        return self.tipo.name

    subtipo: Annotated[SubTipoBranchATM, Doc("branch / ATM subtype")] = Field(
        exclude=True,
        validation_alias="SUB_TIPO",
    )

    @computed_field(alias="subtipoCol")
    def suptipocol(self) -> str:
        return self.subtipo.name

    latitud: float = Field(validation_alias="LATITUD")
    longitud: float = Field(validation_alias="LONGITUD")

    direccion: str = Field(validation_alias="DIRECCION")

    horario_atencion: Optional[HorarioAtencion] = Field(
        exclude=True,
        validation_alias="HORARIO",
    )

    @computed_field(alias="horarioAtencionCol")
    def horario_atencioncol(self) -> str:
        return None if self.horario_atencion is None else self.horario_atencion.name

    @field_validator("*", mode="before")
    def strip_props(string):
        return (
            string
            if not isinstance(string, str)
            else re.sub(r"\s+", " ", string).strip()
        )
