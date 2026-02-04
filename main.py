import os
import csv
import json

from src.dtos.bmsc import BmscBranchATM
from src.dtos.bisa import BisaBranchATM
from src.dtos.baneco import BanecoBranchATM
from src.dtos.bancosol import BancoSolBranchATM

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
    "atms.json",
    "branches.json",
    "sol_amigo.json",
    "sol_amigo_express.json",
]

branchatms: list[BancoSolBranchATM] = []

for department in departments:
    for filename in filenames:
        filepath = f"assets/bancosol/{department.lower()}/{filename}"

        if not os.path.exists(filepath):
            continue

        with open(
            mode="r",
            file=filepath,
            encoding="utf-8",
        ) as jsonfile:
            jdata = json.load(jsonfile)
            branchatms.extend(
                [BancoSolBranchATM.model_validate(jitem) for jitem in jdata]
            )

# rows = []
# filters = []
# for branchatm in branchatms:
#     if branchatm.locality.name not in filters:
#         rows.append(branchatm.model_dump())
#         filters.append(branchatm.locality.name)

# generating csv
rows = [branchatm.model_dump() for branchatm in branchatms]
headers = [key for key in branchatms[0].model_dump().keys()]

with open(
    mode="w",
    newline="",
    encoding="utf-8",
    file=f"assets/bancosol/branchatms.csv",
) as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    writer.writeheader()
    writer.writerows(rows)
