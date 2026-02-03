from enum import IntEnum


class BnbTipoEntidadId(IntEnum):
    OFICINA = 1
    CAJERO_AUTOMATICO = 2


class BnbSubtipoEntidadId(IntEnum):
    AGENCIA = 3
    AUTO_BANCO = 1
    BNB_EXPRESS = 5
    OFICINA_EXTERNA = 6
    BNB_MULTICENTRO = 8
    CAJERO_AUTOMATICO = 0
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
