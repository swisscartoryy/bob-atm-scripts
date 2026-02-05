import re

from typing import Optional
from pydantic import BaseModel, Field, model_validator, computed_field

from .const import TipoCajero, TipoPuntoAtencion


class BancoUnionPuntosAtencionRoot(BaseModel):
    atm: list[BancoUnionBranchATM] = Field(validation_alias="Atm")
    agencia: list[BancoUnionBranchATM] = Field(validation_alias="Agencia")

    @model_validator(mode="after")
    def asignar_punto_atencion(self) -> BancoUnionPuntosAtencionRoot:
        for atm in self.atm:
            atm.punto_atencion = "Atm"

        for agencia in self.agencia:
            agencia.punto_atencion = "Agencia"

        return self


class BancoUnionBranchATM(BaseModel):
    id: int = Field(validation_alias="Identificacion")
    descripcion: str = Field(validation_alias="Descripcion")

    latitud: float = Field(validation_alias="Latitud")
    longitud: float = Field(validation_alias="Longitud")

    icono: int = Field(validation_alias="Icono", exclude=True)
    direccion: str = Field(validation_alias="Direccion")

    tipo_cajero: Optional[TipoCajero] = Field(
        exclude=True,
        validation_alias="TipoCajero",
    )

    @computed_field
    def subtipo(self) -> Optional[str]:
        return None if self.tipo_cajero is None else self.tipo_cajero.upper()

    grafico: Optional[str] = Field(exclude=True, validation_alias="Grafico")
    telefono: Optional[str] = Field(None, validation_alias="Telefono")

    punto_atencion: Optional[TipoPuntoAtencion] = Field(
        exclude=True,
        validation_alias="PuntoAtencion",
    )

    @computed_field
    def tipo(self) -> Optional[str]:
        return None if self.punto_atencion is None else self.punto_atencion.upper()

    dias_semana: str = Field(validation_alias="DiasSemana", exclude=True)

    @computed_field
    def horario_atencion(self) -> str:
        dias_semana = re.sub(r"\s+", " ", self.dias_semana).strip()
        return dias_semana.replace("HORAS", "HORAS;").strip(";")

    sabado: Optional[str] = Field(validation_alias="Sabado", exclude=True)
    domingo: Optional[str] = Field(validation_alias="Domingo", exclude=True)

    caja: Optional[str] = Field(validation_alias="Caja", exclude=True)
    codigo: Optional[str] = Field(validation_alias="Codigo", exclude=True)
    plataforma: Optional[str] = Field(validation_alias="Plataforma", exclude=True)
