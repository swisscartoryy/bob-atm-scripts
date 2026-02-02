# type: ignore
from annotated_doc import Doc

from typing import Annotated
from pydantic import BaseModel, Field

from .const import CiudadBolivia, DepartamentoBolivia, TipoPuntoAtencionATM


class CmsTimeRange(BaseModel):
    id: str = Field(exclude=True)

    open: Annotated[str, Doc("opening hours (eg. '08:00', '24hrs')")]
    close: Annotated[str, Doc("closing time (eg. '18:00', '24hrs')")]

    is_open: bool = Field(
        validation_alias="isOpen",
        serialization_alias="isOpen",
    )


class HorarioAtencionCms(BaseModel):
    monday: list[CmsTimeRange]
    tuesday: list[CmsTimeRange]
    wednesday: list[CmsTimeRange]
    thursday: list[CmsTimeRange]

    friday: list[CmsTimeRange]
    saturday: list[CmsTimeRange]
    sunday: list[CmsTimeRange]


class BmscATM(BaseModel):
    id: int
    titulo: str

    zona: str
    direccion: str

    codigo: str
    codigo_asfi: str = Field(validation_alias="codigoAsfi")

    latitud: float
    longitud: float

    ciudad: CiudadBolivia
    departamento: DepartamentoBolivia = Field(exclude=True)

    discapacitados: bool
    deposito_cheque: bool = Field(validation_alias="depositoCheque")
    deposito_efectivo: bool = Field(validation_alias="depositoEfectivo")

    horario_atencion: str = Field(validation_alias="horarioAtencion")
    estado_aprobacion: Annotated[str, Doc("ov. Aprobado")] = Field(
        validation_alias="estadoDeAprobacion"
    )

    monedas_disponibles: Annotated[str, Doc("eg. BOLIVIA, BOLIVIANOS, Bolivianos")] = (
        Field(validation_alias="monedasDisponibles")
    )

    telefono_emergencia: str = Field(validation_alias="telefonoEmergencia")
    servicios_ofertados: str = Field(validation_alias="serviciosOfertados")

    tipo_punto_atencion: TipoPuntoAtencionATM = Field(
        validation_alias="tipoPuntoAtencion"
    )

    horario_atencioncms_string: Annotated[
        str, Doc("horario atencion cms json string")
    ] = Field(validation_alias="horarioAtencionCms", exclude=True)

    @property
    def horario_atencioncms(self) -> Annotated[
        HorarioAtencionCms,
        Doc("horario atencion cms"),
    ]:
        return HorarioAtencionCms.model_validate_json(self.horario_atencioncms_string)
