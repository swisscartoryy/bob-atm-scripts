import csv
import json

# from scripts.bg import GanaBranchATM
from scripts.bisa import BisaBranchATM

with open(
    mode="r",
    encoding="utf-8",
    file="assets/bisa/branchatms.json",
) as file:
    json_branchatms = json.load(file)
    branchatms = [BisaBranchATM(**json_branchatm) for json_branchatm in json_branchatms]

headers = [key for key in branchatms[0].model_dump().keys()]

cityids: list[int] = []
stateids: list[int] = []
valuetypes: list[int] = []

rows: list = []
for branchatm in branchatms:
    if branchatm.city is not None and branchatm.city.city_id not in cityids:
        cityids.append(branchatm.city.city_id)
        valuetypes.append(branchatm.type.value)

        # print(branchatm.city.name)
        if branchatm.state is not None:
            stateids.append(branchatm.state.state_id)

        rows.append(branchatm.model_dump())
    # if branchatm.state is not None and branchatm.state.state_id not in stateids:
    #     stateids.append(branchatm.state.state_id)
    #     valuetypes.append(branchatm.type.value)

    #     if branchatm.city is not None:
    #         cityids.append(branchatm.city.city_id)

    #     rows.append(branchatm.model_dump())
    # elif branchatm.type.value not in valuetypes:
    #     valuetypes.append(branchatm.type.value)

    #     if branchatm.state is not None:
    #         stateids.append(branchatm.state.state_id)

    #     if branchatm.city is not None:
    #         cityids.append(branchatm.city.city_id)

    #     print(branchatm.poitype)
    #     rows.append(branchatm.model_dump())

print(stateids, len(rows))

# rows = [branchatm.model_dump() for branchatm in branchatms]

with open(
    mode="w",
    newline="",
    encoding="utf-8",
    file="assets/bisa/branchatms.csv",
) as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    writer.writerows(rows)
