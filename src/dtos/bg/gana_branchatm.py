# type: ignore
import re

from annotated_doc import Doc

from typing import Annotated, Optional
from pydantic import BaseModel, field_validator, Field

from .enums import TipoBranchATM, SubTipoBranchATM, HorarioAtencion


class GanaBranchATM(BaseModel):
    id: int = Field(validation_alias="ID")

    nombre: str = Field(validation_alias="NOMBRE")
    descripcion: str = Field(validation_alias="DESCRIPCION")

    telefono: Annotated[str, Doc("contact phonenumber")] = Field(
        validation_alias="TELEFONO"
    )

    tipo: Annotated[TipoBranchATM, Doc("branch / ATM")] = Field(validation_alias="TIPO")
    subtipo: Annotated[SubTipoBranchATM, Doc("branch / ATM subtype")] = Field(
        validation_alias="SUB_TIPO"
    )

    latitud: float = Field(validation_alias="LATITUD")
    longitud: float = Field(validation_alias="LONGITUD")

    direccion: str = Field(validation_alias="DIRECCION")
    horario_atencion: Optional[HorarioAtencion] = Field(validation_alias="HORARIO")

    @field_validator("*", mode="before")
    def strip_props(string):
        return (
            string
            if not isinstance(string, str)
            else re.sub(r"\s+", " ", string).strip()
        )
