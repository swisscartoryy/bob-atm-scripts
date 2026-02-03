import csv
import json

from src.dtos.bisa import BisaBranchATM
from src.dtos.bmsc import BmscATM, BmscBranch
from src.dtos.bnb import BnbDepartamento, BnbBranchATM

filename = "assets/bnb/branchatms.json"

# opening json
with open(
    mode="r",
    file=filename,
    encoding="utf-8",
) as jsonfile:
    jbranchatms = json.load(jsonfile)
    departamentos = [
        BnbDepartamento.model_validate(jbranchatm) for jbranchatm in jbranchatms
    ]

    branchatms = [
        branchatm
        for departamento in departamentos
        for branchatm in departamento.detalles
    ]

# filters
# rows = []
# filters = []
# for branchatm in branchatms:
#     if branchatm.subtipo not in filters:
#         filters.append(branchatm.subtipo)
#         rows.append(branchatm.model_dump())
# print(len(filters), filters)

# writting csv
rows = [branchatm.model_dump() for branchatm in branchatms]
headers = [key for key in branchatms[0].model_dump().keys()]

with open(
    mode="w",
    newline="",
    encoding="utf-8",
    file=f"{filename[:-len(".json")]}.csv",
) as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    writer.writerows(rows)
