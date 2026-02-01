# type: ignore
import re

from enum import Enum
from typing import Annotated

from annotated_doc import Doc
from pydantic import BaseModel, field_validator


class Tipo(Enum):
    ATM: Annotated[str, Doc("Terminal o cajero automático")] = "T"
    AGENCIA: Annotated[str, Doc("Agencia bancaria o sucursal")] = "A"


class SubTipo(Enum):
    ATM_L: Annotated[str, Doc("ATM tipo L (especial)")] = "L"
    KIOSCO: Annotated[str, Doc("Kiosco de autoservicio")] = "K"
    INFANTIL: Annotated[str, Doc("ATM infantil/interactivo")] = "I"
    KIOSCO_S: Annotated[str, Doc("Kiosco sub-Tipo S")] = "S"
    AGENCIA_B: Annotated[str, Doc("Subtipo interno B de agencia")] = "B"
    AGENCIA_D: Annotated[str, Doc("Subtipo interno D de agencia")] = "D"
    ATM_ESTANDAR: Annotated[str, Doc("ATM estándar")] = "T"
    ATM_ESPECIAL: Annotated[
        str, Doc("ATM especial (externo o con características distintas)")
    ] = "E"
    AGENCIA_NORMAL: Annotated[str, Doc("Agencia estándar")] = "A"
    DISCAPACITADOS: Annotated[str, Doc("ATM adaptado para discapacitados")] = "J"


class Horario(Enum):
    SI: Annotated[str, Doc("Ubicación abierta / disponible")] = "S"
    NO: Annotated[str, Doc("Ubicación cerrada / no disponible")] = "N"


class GanaBranchATM(BaseModel):
    ID: Annotated[int, Doc("Identificador único interno de la ubicación")]

    NOMBRE: Annotated[str, Doc("Nombre comercial o identificador visible")]
    DESCRIPCION: Annotated[str, Doc("Descripción funcional del punto")]

    HORARIO: Annotated[Horario | None, Doc("Disponibilidad u horario de atención")]
    TELEFONO: Annotated[str, Doc("Número telefónico de contacto")]

    TIPO: Annotated[Tipo, Doc("Tipo principal: ATM o Agencia")]
    SUB_TIPO: Annotated[SubTipo, Doc("Clasificación interna del tipo")]

    LATITUD: Annotated[float, Doc("Latitud geográfica en formato decimal")]
    LONGITUD: Annotated[float, Doc("Longitud geográfica en formato decimal")]
    DIRECCION: Annotated[str, Doc("Dirección física completa")]

    @field_validator("*", mode="before")
    def normalize_string(string):
        return (
            string
            if not isinstance(string, str)
            else re.sub(r"\s+", " ", string.strip())
        )
