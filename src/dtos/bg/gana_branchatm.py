# type: ignore
import re

from enum import Enum
from typing import Annotated, Optional

from annotated_doc import Doc
from pydantic import BaseModel, field_validator, Field


class TipoBranchATM(Enum):
    ATM = "T"
    AGENCIA = "A"


class SubTipoBranchATM(Enum):
    AGENCIA_B = "B"
    AGENCIA_D = "D"
    AGENCIA_NORMAL = "A"

    ATM_ESPECIAL = "E"
    ATM_ESTANDAR = "T"

    KIOSCO: Annotated[str, Doc("autoservice kiosk")] = "K"
    KIOSCO_S: Annotated[str, Doc("Kiosk subtype S")] = "S"

    ATM_L: Annotated[str, Doc("ATM type L")] = "L"
    INFANTIL: Annotated[str, Doc("childfriendly ATM")] = "I"
    DISCAPACITADOS: Annotated[str, Doc("disablefriendly ATM")] = "J"


class HorarioAtencion(Enum):
    SI: Annotated[str, Doc("open / available")] = "S"
    NO: Annotated[str, Doc("closed / unavailable")] = "N"


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
    def normalize_string(string):
        return (
            string
            if not isinstance(string, str)
            else re.sub(r"\s+", " ", string.strip())
        )
