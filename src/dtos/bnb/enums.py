from enum import IntEnum


class BnbTipoEntidadId(IntEnum):
    ATM = 2
    AGENCIA = 1


class BnbSubtipoEntidadId(IntEnum):
    ATM = 0
    AGENCIA = 3
    AUTO_BANCO = 1
    BNB_EXPRESS = 5
    OFICINA_EXTERNA = 6
    BNB_MULTICENTRO = 8
    OFICINA_PRINCIPAL = 2
    PUNTO_PROMOCIONAL = 4


class BnbDepartamentoId(IntEnum):
    BENI = 801
    PANDO = 901
    ORURO = 401
    LA_PAZ = 206
    TARIJA = 601
    POTOSI = 510
    SANTA_CRUZ = 701
    CHUQUISACA = 101
    COCHABAMBA = 301
