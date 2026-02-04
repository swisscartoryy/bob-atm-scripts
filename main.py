import os
import csv
import json

from typing import Any
from src.dtos.bancounion import BancoUnionBranchATM, BancoUnionPuntosAtencion

departments = [
    "BENI",
    "PANDO",
    "ORURO",
    "LA_PAZ",
    "TARIJA",
    "POTOSI",
    "SANTA_CRUZ",
    "CHUQUISACA",
    "COCHABAMBA",
]

filenames = [
    "branchatms.json",
]

branchatms: list[BancoUnionBranchATM] = []

for department in departments:
    for filename in filenames:
        filepath = f"assets/bancounion/{department.lower()}/{filename}"

        if not os.path.exists(filepath):
            continue

        with open(
            mode="r",
            file=filepath,
            encoding="utf-8",
        ) as jsonfile:
            jdata = json.load(jsonfile)
            puntos_atencion = BancoUnionPuntosAtencion.model_validate(jdata)

            branchatms.extend(puntos_atencion.atm)
            branchatms.extend(puntos_atencion.agencia)

# rows = []
# filters = []
# for branchatm in branchatms:
#     if branchatm.grafico not in filters:
#         rows.append(branchatm.model_dump())
#         filters.append(branchatm.grafico)
#
# print(len(filters), filters)

# generating csv
rows = [branchatm.model_dump() for branchatm in branchatms]
headers = [key for key in branchatms[0].model_dump().keys()]

with open(
    mode="w",
    newline="",
    encoding="utf-8",
    file=f"assets/bancounion/branchatms.csv",
) as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    writer.writeheader()
    writer.writerows(rows)
