import csv
import json

# from scripts.bg import GanaBranchATM
from src.dtos.bisa import BisaBranchATM

with open(
    mode="r",
    encoding="utf-8",
    file="assets/bisa/branchatms.json",
) as file:
    json_branchatms = json.load(file)
    branchatms = [BisaBranchATM(**json_branchatm) for json_branchatm in json_branchatms]

rows = [branchatm.model_dump() for branchatm in branchatms]
headers = [key for key in branchatms[0].model_dump().keys()]

with open(
    mode="w",
    newline="",
    encoding="utf-8",
    file="assets/bisa/branchatms.csv",
) as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    writer.writerows(rows)
