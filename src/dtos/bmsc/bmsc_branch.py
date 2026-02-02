from annotated_doc import Doc

from typing import Annotated, Optional, Literal
from pydantic import BaseModel, Field, computed_field

from .bmsc_atm import HorarioAtencionCms
from .const import CiudadBolivia, DepartamentoBolivia, TipoPuntoAtencionBranch

PosValue = Literal["(SIN POS)", "NO"]


class BmscBranch(BaseModel):
    id: int
    codigo: str

    pos: PosValue = Field(exclude=True)
    zona: str = Field(exclude=True)

    @computed_field(alias="tienePos")
    @property
    def tiene_pos(self) -> bool:
        return self.pos == "NO"

    titulo: str
    telefono: str
    direccion: str

    latitud: float
    longitud: float

    es_autobanco: bool = Field(validation_alias="esAutoBanco")
    es_principal: bool = Field(validation_alias="esPrincipal")

    ciudad: CiudadBolivia
    departamento: DepartamentoBolivia

    horario_atencion: str = Field(validation_alias="horarioAtencion")
    estado_aprobacion: str = Field(validation_alias="estadoDeAprobacion")

    tipo_punto_atencion1: Optional[TipoPuntoAtencionBranch] = Field(
        validation_alias="tipoPuntoAtencion1"
    )

    tipo_punto_atencion2: Optional[TipoPuntoAtencionBranch] = Field(
        validation_alias="tipoPuntoAtencion2"
    )

    servicios_ofertados: str = Field(validation_alias="serviciosOfertados")

    horario_atencioncms_string: Annotated[
        str, Doc("horario atencion cms json string")
    ] = Field(validation_alias="horarioAtencionCms", exclude=True)

    @property
    def horario_atencioncms(self) -> Annotated[
        HorarioAtencionCms,
        Doc("horario atencion cms"),
    ]:
        return HorarioAtencionCms.model_validate_json(self.horario_atencioncms_string)
