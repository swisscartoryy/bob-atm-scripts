from typing import Literal

PosValue = Literal[
    "NO",
    "(SIN POS)",
]

TipoPuntoAtencionBranch = Literal[
    "Sucursal",
    "Agencia Fija",
    "Oficina Central",
    "Oficina Externa",
    "Punto Promocional Fijo",
]

DepartamentoBolivia = Literal[
    "Beni",
    "Oruro",
    "Pando",
    "Potosí",
    "Tarija",
    "La Paz",
    "Santa Cruz",
    "Chuquisaca",
    "Cochabamba",
]

TipoPuntoAtencionATM = Literal[
    "Cajero Automático Interno",
    "Cajero Automático Especial Interno",
    "Cajero Automático Externo - Sin Recinto",
    "Cajero Automático Externo - Con Recinto",
    "Cajero Automático Especial Externo - Con Recinto",
    "Cajero Automático Especial Externo - Sin Recinto",
    "Cajero Automático para Personas con Discapacidad Interno",
]

TipoPuntoAtencion = TipoPuntoAtencionATM | TipoPuntoAtencionBranch
