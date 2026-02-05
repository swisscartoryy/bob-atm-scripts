# type: ignore
from enum import StrEnum
from typing import Annotated

from annotated_doc import Doc


class TipoBranchATM(StrEnum):
    ATM = "T"
    AGENCIA = "A"


class SubTipoBranchATM(StrEnum):
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


class HorarioAtencion(StrEnum):
    SI: Annotated[str, Doc("open / available")] = "S"
    NO: Annotated[str, Doc("closed / unavailable")] = "N"
