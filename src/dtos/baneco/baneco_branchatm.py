import re

from typing import Literal
from pydantic import BaseModel, field_validator, Field, computed_field

from .enums import (
    BanecoTipoEntidad,
    BanecoTipoMiSocio,
    BanecoDepartamentoId,
    BanecoEstadoServicio,
    BanecoTipoBancaPersona,
)


Moneda = Literal["Bs.", "Bs. $us.", "0"]
TipoDireccion = Literal["Calle", "Av.", ""]


class BanecoBranchATM(BaseModel):
    id: int = Field(validation_alias="codigo")

    tipo: BanecoTipoEntidad = Field(exclude=True)
    nombre: str

    @computed_field(alias="tipoEntidad")
    def tipo_entidad(self) -> str:
        return BanecoTipoEntidad(self.tipo).name

    departamento: str = Field(validation_alias="dpto", exclude=True)
    cod_departamento: BanecoDepartamentoId = Field(
        exclude=True,
        validation_alias="coddpto",
    )

    @computed_field(alias="nombreDepartamento")
    def nombre_departamento(self) -> str:
        return BanecoDepartamentoId(self.cod_departamento).name

    zona: str
    tipodir: TipoDireccion

    latitud: float
    longitud: float
    direccion: str

    moneda: Moneda
    horarios: str
    telefonos: str

    misocio: BanecoTipoMiSocio = Field(exclude=True)

    @computed_field(alias="tipoMiSocio")
    def tipo_misocio(self) -> str:
        return BanecoTipoMiSocio(self.misocio).name

    bancapersona: BanecoTipoBancaPersona = Field(exclude=True)

    @computed_field(alias="tipoBancaPersona")
    def tipo_bancapersona(self) -> str:
        return BanecoTipoBancaPersona(self.bancapersona).name

    depositoefectivo: BanecoEstadoServicio = Field(exclude=True)

    @computed_field(alias="depositoEfectivo")
    def tiene_depositoefectivo(self) -> str:
        return BanecoEstadoServicio(self.depositoefectivo).name

    personasdiscapacidad: BanecoEstadoServicio = Field(exclude=True)

    @computed_field(alias="personasDiscapacidad")
    def atencion_personasdiscapacidad(self) -> str:
        return BanecoEstadoServicio(self.personasdiscapacidad).name

    @field_validator("*", mode="before")
    def strip_props(cls, prop_value):
        return (
            prop_value
            if not isinstance(prop_value, str)
            else re.sub(r"\s+", " ", prop_value).strip()
        )
