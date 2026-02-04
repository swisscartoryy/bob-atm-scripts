import re

from annotated_doc import Doc

from typing import Annotated, Optional
from pydantic import BaseModel, Field, computed_field

from .const import PosValue, TipoPuntoAtencion, DepartamentoBolivia

normalized_vowels = str.maketrans(
    "áéíóúÁÉÍÓÚ",
    "aeiouAEIOU",
)


class CmsTimeRange(BaseModel):
    id: str = Field(exclude=True)

    open: Annotated[str, Doc("opening hours (eg. '08:00', '24hrs')")]
    close: Annotated[str, Doc("closing time (eg. '18:00', '24hrs')")]

    is_open: Optional[bool] = Field(
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


class BmscBranchATM(BaseModel):
    id: int
    titulo: str

    pos: Optional[PosValue] = Field(None, exclude=True)

    @computed_field(alias="tienePos")
    @property
    def tiene_pos(self) -> bool:
        return self.pos == "NO"

    zona: str
    direccion: str

    codigo: str
    codigo_asfi: Optional[str] = Field(None, validation_alias="codigoAsfi")

    latitud: float
    longitud: float

    ciudad: str
    departamento: DepartamentoBolivia = Field(exclude=True)

    @computed_field(alias="nombreDepartamento")
    def nombre_departamento(self) -> str:
        return re.sub(
            r"\s+", "_", self.departamento.translate(normalized_vowels)
        ).upper()

    es_autobanco: Optional[bool] = Field(None, validation_alias="esAutoBanco")
    es_principal: Optional[bool] = Field(None, validation_alias="esPrincipal")

    discapacitados: Optional[bool] = Field(None)
    deposito_cheque: Optional[bool] = Field(None, validation_alias="depositoCheque")
    deposito_efectivo: Optional[bool] = Field(None, validation_alias="depositoEfectivo")

    horario_atencion: str = Field(validation_alias="horarioAtencion")
    estado_aprobacion: Annotated[str, Doc("ov. Aprobado")] = Field(
        validation_alias="estadoDeAprobacion",
    )

    monedas_disponibles: Annotated[
        Optional[str], Doc("eg. BOLIVIA, BOLIVIANOS, Bolivianos")
    ] = Field(None, validation_alias="monedasDisponibles")

    telefono: str = Field(validation_alias="telefono")
    servicios_ofertados: str = Field(validation_alias="serviciosOfertados")

    tipo_punto_atencion: Optional[TipoPuntoAtencion] = Field(
        default=None,
        exclude=True,
        validation_alias="tipoPuntoAtencion",
    )

    @computed_field(alias="puntoAtencion")
    def punto_atencion(self) -> Optional[str]:
        punto_atencion = self.tipo_punto_atencion

        if punto_atencion is None:
            return None

        return re.sub(
            r"\s+", "_", punto_atencion.translate(normalized_vowels).replace("-", " ")
        ).upper()

    horario_atencioncms_string: Annotated[
        str, Doc("horario atencion cms json string")
    ] = Field(validation_alias="horarioAtencionCms", exclude=True)

    @property
    def horario_atencioncms(self) -> Annotated[
        HorarioAtencionCms,
        Doc("horario atencion cms"),
    ]:
        return HorarioAtencionCms.model_validate_json(self.horario_atencioncms_string)
