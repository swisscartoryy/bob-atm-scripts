import re

from annotated_doc import Doc

from typing import Annotated, Optional, get_args
from pydantic import BaseModel, Field, computed_field

from .const import (
    PosValue,
    TipoPuntoAtencion,
    DepartamentoBolivia,
    TipoPuntoAtencionATM,
    TipoPuntoAtencionBranch,
)

transvowels = str.maketrans(
    "áéíóúÁÉÍÓÚ",
    "aeiouAEIOU",
)


class CmsTimeRange(BaseModel):
    id: str = Field("", exclude=True)

    open: Annotated[str, Doc("opening hours (eg. '08:00', '24hrs')")]
    close: Annotated[str, Doc("closing time (eg. '18:00', '24hrs')")]

    is_open: Optional[bool] = Field(
        default=None,
        validation_alias="isOpen",
        serialization_alias="isOpen",
    )

    def to_string(self) -> str:
        return (
            self.open
            if self.open == self.close
            else f"{self.open[:2]}:{self.open[2:]} - {self.close[:2]}:{self.close[2:]}"
        )


class HorarioAtencionCms(BaseModel):
    monday: list[CmsTimeRange]
    tuesday: list[CmsTimeRange]
    wednesday: list[CmsTimeRange]
    thursday: list[CmsTimeRange]

    friday: list[CmsTimeRange]
    saturday: list[CmsTimeRange]
    sunday: list[CmsTimeRange]

    def to_string(self) -> str:
        weekdays = [
            f"{weekday}: {",".join(f"{CmsTimeRange.model_validate(tr).to_string()}" for tr in timeranges)}"
            for weekday, timeranges in self.model_dump().items()
        ]

        return ";".join(weekdays)


class BmscBranchATM(BaseModel):
    id: int
    nombre: str = Field(validation_alias="titulo")

    pos: Optional[PosValue] = Field(None, exclude=True)

    zona: str = Field(exclude=True)
    direccion: str

    codigo: str = Field(exclude=True)
    codigo_asfi: Optional[str] = Field(
        default=None,
        exclude=True,
        validation_alias="codigoAsfi",
    )

    latitud: float
    longitud: float

    nombre_ciudad: str = Field(validation_alias="ciudad", exclude=True)

    @computed_field
    def ciudad(self) -> str:
        return self.nombre_ciudad.replace(" ", "_").translate(transvowels).upper()

    nombre_departamento: DepartamentoBolivia = Field(
        exclude=True,
        validation_alias="departamento",
    )

    @computed_field
    def departamento(self) -> str:
        return re.sub(
            r"\s+", "_", self.nombre_departamento.translate(transvowels)
        ).upper()

    es_autobanco: Optional[bool] = Field(
        default=None,
        exclude=True,
        validation_alias="esAutoBanco",
    )

    es_principal: Optional[bool] = Field(
        default=None,
        exclude=True,
        validation_alias="esPrincipal",
    )

    discapacitados: Optional[bool] = Field(None, exclude=True)

    deposito_cheque: Optional[bool] = Field(
        default=None,
        exclude=True,
        validation_alias="depositoCheque",
    )

    deposito_efectivo: Optional[bool] = Field(
        default=None,
        exclude=True,
        validation_alias="depositoEfectivo",
    )

    horario_atencion: str = Field(validation_alias="horarioAtencion", exclude=True)
    estado_aprobacion: Annotated[str, Doc("ov. Aprobado")] = Field(
        exclude=True,
        validation_alias="estadoDeAprobacion",
    )

    monedas_disponibles: Annotated[
        Optional[str], Doc("eg. BOLIVIA, BOLIVIANOS, Bolivianos")
    ] = Field(None, exclude=True, validation_alias="monedasDisponibles")

    telefono: str = Field(validation_alias="telefono")
    servicios_ofertados: str = Field(validation_alias="serviciosOfertados")

    tipopoi: Optional[TipoPuntoAtencion] = Field(
        default=None,
        exclude=True,
        validation_alias="tipoPuntoAtencion",
    )

    @computed_field
    def tipo(self) -> Optional[str]:
        tipo: Optional[str] = None
        tipo_branches: list[str] = list(get_args(TipoPuntoAtencionBranch))

        if not self.tipopoi is None:
            if self.tipopoi in tipo_branches:
                tipo = "AGENCIA"
            elif self.tipopoi in get_args(TipoPuntoAtencionATM):
                tipo = "ATM"
        else:
            for tipo_branch in tipo_branches:
                if self.nombre.startswith(tipo_branch.upper()):
                    tipo = "AGENCIA"
                    break

        return tipo

    @computed_field
    def subtipo(self) -> Optional[str]:
        subtipo = None

        if not self.tipopoi is None:
            subtipo = (
                re.sub(r"\s+", "_", self.tipopoi.translate(transvowels))
                .upper()
                .replace("-", "")
                .replace("CAJERO_AUTOMATICO", "ATM")
            )
        else:
            tipo_branches: list[str] = list(get_args(TipoPuntoAtencionBranch))

            for tipo_branch in tipo_branches:
                tipo_branch = tipo_branch.upper()
                if self.nombre.startswith(tipo_branch):
                    subtipo = re.sub(r"\s+", "_", tipo_branch)

        return subtipo

    horario_atencioncms_string: Annotated[
        str, Doc("horario atencion cms json string")
    ] = Field(validation_alias="horarioAtencionCms", exclude=True)

    @computed_field
    def horario_atencioncms(self) -> Annotated[str, Doc("horario atencion cms")]:
        return HorarioAtencionCms.model_validate_json(
            self.horario_atencioncms_string
        ).to_string()
