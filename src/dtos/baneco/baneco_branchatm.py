import re

from pydantic import BaseModel, field_validator, Field, computed_field

from .enums import (
    Moneda,
    TipoDireccion,
    BanecoTipoEntidad,
    BanecoTipoMiSocio,
    BanecoDepartamentoId,
    BanecoEstadoServicio,
    BanecoTipoBancaPersona,
)


class BanecoBranchATM(BaseModel):
    id: int = Field(validation_alias="codigo")

    tipo: BanecoTipoEntidad = Field(exclude=True)
    nombre: str

    @computed_field(alias="tipoEntidad")
    def tipocol(self) -> str:
        return BanecoTipoEntidad(self.tipo).name

    departamento: str = Field(validation_alias="dpto", exclude=True)
    cod_departamento: BanecoDepartamentoId = Field(
        exclude=True,
        validation_alias="coddpto",
    )

    @computed_field(alias="departamentoCol")
    def departamentocol(self) -> str:
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

    @computed_field(alias="tieneMiSocio")
    def tiene_misocio(self) -> str:
        return BanecoTipoMiSocio(self.misocio).name

    bancapersona: BanecoTipoBancaPersona = Field(exclude=True)

    @computed_field(alias="tieneBancaPersona")
    def tiene_bancapersona(self) -> str:
        return BanecoTipoBancaPersona(self.bancapersona).name

    depositoefectivo: BanecoEstadoServicio = Field(exclude=True)

    @computed_field(alias="tieneDepositoEfectivo")
    def tiene_depositoefectivo(self) -> str:
        return BanecoEstadoServicio(self.depositoefectivo).name

    personasdiscapacidad: BanecoEstadoServicio = Field(exclude=True)

    @computed_field(alias="atiendePersonasDiscapacidad")
    def atiende_personasdiscapacidad(self) -> str:
        return BanecoEstadoServicio(self.personasdiscapacidad).name

    @field_validator("*", mode="before")
    def strip_props(cls, prop_value):
        return (
            prop_value
            if not isinstance(prop_value, str)
            else re.sub(r"\s+", " ", prop_value).strip()
        )
