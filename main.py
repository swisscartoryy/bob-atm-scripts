import csv
import json

from src.dtos.bmsc import BmscBranchATM
from src.dtos.bisa import BisaBranchATM
from src.dtos.baneco import BanecoBranchATM

filename = "assets/bmsc/branchatms.json"

# opening json
with open(
    mode="r",
    file=filename,
    encoding="utf-8",
) as jsonfile:
    jbranchatms = json.load(jsonfile)
    branchatms = [
        BmscBranchATM.model_validate(jbranchatm) for jbranchatm in jbranchatms
    ]

# rows = []
# filters = []

# for branchatm in branchatms:
#     if branchatm.depositoefectivo not in filters:
#         filters.append(branchatm.depositoefectivo)
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
