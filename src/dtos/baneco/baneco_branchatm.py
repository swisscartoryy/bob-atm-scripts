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

    nombre: str
    tipopoi: BanecoTipoEntidad = Field(exclude=True, validation_alias="tipo")

    @computed_field
    def tipo(self) -> str:
        return BanecoTipoEntidad(self.tipopoi).name

    dpto: str = Field(validation_alias="dpto", exclude=True)
    cod_departamento: BanecoDepartamentoId = Field(
        exclude=True,
        validation_alias="coddpto",
    )

    @computed_field
    def departamento(self) -> str:
        return BanecoDepartamentoId(self.cod_departamento).name

    zona: str = Field(exclude=True)
    tipodir: TipoDireccion = Field(exclude=True)
    direccion: str

    latitud: float
    longitud: float

    moneda: Moneda = Field(exclude=True)
    horarios: str
    telefonos: str

    misocio: BanecoTipoMiSocio = Field(exclude=True)
    bancapersona: BanecoTipoBancaPersona = Field(exclude=True)
    depositoefectivo: BanecoEstadoServicio = Field(exclude=True)
    personasdiscapacidad: BanecoEstadoServicio = Field(exclude=True)

    @field_validator("*", mode="before")
    def strip_props(cls, prop_value):
        return (
            prop_value
            if not isinstance(prop_value, str)
            else re.sub(r"\s+", " ", prop_value).strip()
        )
