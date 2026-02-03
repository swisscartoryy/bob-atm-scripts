import csv
import json

from src.dtos.bmsc import BmscATM, BmscBranch
from src.dtos.bisa import BisaBranchATM
from src.dtos.baneco import BanecoBranchATM

filename = "assets/baneco/atms.json"

# opening json
with open(
    mode="r",
    file=filename,
    encoding="utf-8",
) as jsonfile:
    jbranchatms = json.load(jsonfile)
    branchatms = [BanecoBranchATM.model_validate(jbranchatm) for jbranchatm in jbranchatms]

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
