from typing import Literal

BancoSolOfficeTypeName = Literal[
    "Sucursal",
    "Agencia Fija",
    "Agencia Móvil",
    "Oficina Externa",
    "Ventanilla de Cobranza",
    "Punto Corresponsal no Financiero",
    "Punto Corresponsal No Financiero",
    # ATM
    "Cajero Automático Interno",
    "Cajero Automático Externo - Con Recinto",
    "Cajero Automático Externo - Sin Recinto",
    "Cajero Automático Especial Externo - Sin Recinto",
    "Cajero Automático Especial Externo - Con Recinto",
    "Cajero Automático para personas con discapacidad Externo - Con Recinto",
]

BancoSolOfficeName = Literal[
    "Cajeros",
    "Agencias",
    "Sol amigo",
    "Sol amigo express",
]
