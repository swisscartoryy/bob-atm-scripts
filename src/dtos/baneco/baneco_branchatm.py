from pydantic import BaseModel


class BanecoBranchATM(BaseModel):
    tipo: int  # 1
    codigo: int  # 38

    nombre: str  # ATM Ag. Ingavi
    moneda: str  # Bs.

    dpto: str  # SANTA CRUZ
    coddpto: int  # 7

    zona: str  # CENTRO
    tipodir: str  # Calle
    direccion: str

    latitud: float
    longitud: float

    horarios: str  #
    telefonos: str  #

    misocio: int  # 0
    bancapersona: int  # 0
    depositoefectivo: int  # 2
    personasdiscapacidad: int  # 2
