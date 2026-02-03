from enum import IntEnum


class BanecoEstadoServicio(IntEnum):
    NO = 1
    SI = 2
    NO_APLICA = 0


class BanecoTipoMiSocio(IntEnum):
    SOCIO = 1
    NO_APLICA = 0
    SOCIO_PREMIUM = 2


class BanecoTipoBancaPersona(IntEnum):
    PARCIAL = 1
    COMPLETA = 2
    NO_APLICA = 0


class BanecoTipoEntidad(IntEnum):
    ATM = 1
    AGENCIA = 2


class BanecoDepartamentoId(IntEnum):
    # BENI = 8
    # PANDO = 9
    ORURO = 4
    LA_PAZ = 2
    POTOSI = 5
    TARIJA = 6
    CHUQUISACA = 1
    COCHABAMBA = 3
    SANTA_CRUZ = 7
