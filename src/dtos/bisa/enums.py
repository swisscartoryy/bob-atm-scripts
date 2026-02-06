# type: ignore
from enum import IntEnum
from typing import Annotated


class PointOfInterestId(IntEnum):
    ATM = 1
    AGENCIA = 2
    TERMINAL_AUTOSERVICIO = 3
    AGENCIA_HORARIO_EXTENDIDO = 4


class BoliviaStateId(IntEnum):
    BENI: Annotated[int, Doc("Beni state, Bolivia")] = 9
    PANDO: Annotated[int, Doc("Pando state, Bolivia")] = 8
    ORURO: Annotated[int, Doc("Oruro state, Bolivia")] = 6

    LA_PAZ: Annotated[int, Doc("La Paz state, Bolivia")] = 1
    TARIJA: Annotated[int, Doc("Tarija state, Bolivia")] = 5
    POTOSI: Annotated[int, Doc("Potosí state, Bolivia")] = 7

    SANTA_CRUZ: Annotated[int, Doc("Santa Cruz state, Bolivia")] = 2
    COCHABAMBA: Annotated[int, Doc("Cochabamba state, Bolivia")] = 3
    CHUQUISACA: Annotated[int, Doc("Chuquisaca state, Bolivia")] = 4


class BoliviaCityId(IntEnum):
    LA_PAZ: Annotated[int, Doc("La Paz city, La Paz")] = 1
    EL_ALTO: Annotated[int, Doc("El Alto city, La Paz")] = 3

    ORURO: Annotated[int, Doc("Oruro city, Oruro")] = 15
    SUCRE: Annotated[int, Doc("Sucre city, Chuquisaca")] = 11

    COBIJA: Annotated[int, Doc("Cobija city, Pando")] = 17
    POTOSI: Annotated[int, Doc("Potosí city, Potosí")] = 16
    TRINIDAD: Annotated[int, Doc("Trinidad city, Beni")] = 18

    TARIJA: Annotated[int, Doc("Tarija city, Tarija")] = 12
    YACUIBA: Annotated[int, Doc("Yacuiba city, Tarija")] = 14
    VILLAMONTES: Annotated[int, Doc("Villamontes city, Tarija")] = 13

    COCHABAMBA: Annotated[int, Doc("Cochabamba city, Cochabamba")] = 9
    QUILLA_COLLO: Annotated[int, Doc("Quillacollo city, Cochabamba")] = 10

    CAMIRI: Annotated[int, Doc("Camiri city, Santa Cruz")] = 8
    MONTERO: Annotated[int, Doc("Montero city, Santa Cruz")] = 5
    SANTA_CRUZ: Annotated[int, Doc("Santa Cruz city, Santa Cruz")] = 4
    PUERTO_SUAREZ: Annotated[int, Doc("Puerto Suárez city, Santa Cruz")] = 6
    ARROYO_CONCEPCION: Annotated[int, Doc("Arroyo Concepción city, Santa Cruz")] = 7
