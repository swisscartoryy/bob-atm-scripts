from typing import Annotated
from annotated_doc import Doc

from pydantic import BaseModel, Field


class CmsTimeRange(BaseModel):
    id: str

    open: Annotated[str, Doc("opening hours (eg. '08:00', '24hrs')")]
    close: Annotated[str, Doc("closing time (eg. '18:00', '24hrs')")]

    is_open: bool = Field(validation_alias="isOpen")


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

    discapacitados: bool
    deposito_cheque: bool = Field(validation_alias="depositoCheque")
    deposito_efectivo: bool = Field(validation_alias="depositoEfectivo")

    ciudad: str
    horario_atencion: str = Field(validation_alias="horarioAtencion")
    estado_aprobacion: str = Field(validation_alias="estadoDeAprobacion")
    monedas_disponibles: str = Field(validation_alias="monedasDisponibles")

    latitud: float
    longitud: float

    codigo: str
    codigo_asfi: str = Field(validation_alias="codigoAsfi")
    departamento: str

    tipo_punto_atencion: str = Field(validation_alias="tipoPuntoAtencion")
    telefono_emergencia: str = Field(validation_alias="telefonoEmergencia")
    servicios_ofertados: str = Field(validation_alias="serviciosOfertados")

    horario_atencioncms_string: str = Field(alias="horarioAtencionCms", exclude=True)

    @property
    def horario_atencioncms(self) -> BmscATM:
        return self.model_validate_json(self.horario_atencioncms_string)
