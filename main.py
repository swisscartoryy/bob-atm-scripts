import os

import csv
import json

from typing import Literal

from src.dtos.bg import GanaBranchATM

from src.dtos.bisa import BisaBranchATM
from src.dtos.bmsc import BmscBranchATM

from src.dtos.baneco import BanecoBranchATM
from src.dtos.bancosol import BancoSolBranchATM

from src.dtos.bnb import BnbBranchATM, BnbDepartamentoRoot
from src.dtos.bancounion import BancoUnionBranchATM, BancoUnionPuntosAtencionRoot


BankCode = Literal[
    "bg",
    "bnb",
    "bmsc",
    "bisa",
    "baneco",
    "bancosol",
    "bancounion",
]

bank_branchatm: dict[BankCode, type] = {
    "bg": GanaBranchATM,
    "bnb": BnbBranchATM,
    "bmsc": BmscBranchATM,
    "bisa": BisaBranchATM,
    "baneco": BanecoBranchATM,
    "bancosol": BancoSolBranchATM,
    "bancounion": BancoUnionBranchATM,
}

filenames = [
    "atms.json",
    "branches.json",
    "sol_amigo.json",
    "branchatms.json",
    "sol_amigo_express.json",
]

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


def jdata_from_jsonfile(filename: str):
    with open(mode="r", file=filename, encoding="utf-8") as jsonfile:
        jdata = json.load(jsonfile)

    return jdata


def write_data_to_csvfile(filename: str, data: list):
    rows = [item.model_dump() for item in data]
    headers = [key for key in data[0].model_dump().keys()]

    with open(mode="w", newline="", file=filename, encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

        print(filename, "generated")


for bankcode in bank_branchatm.keys():
    branchatms: list = []

    for filename in filenames:
        filepath = f"assets/{bankcode}/{filename}"

        if not os.path.exists(filepath):
            for department in departments:
                filepath = f"assets/{bankcode}/{department.lower()}/{filename}"

                if not os.path.exists(filepath):
                    continue

                jdata = jdata_from_jsonfile(filename=filepath)

                if bankcode == "bancounion":
                    puntos_atencion = BancoUnionPuntosAtencionRoot.model_validate(jdata)
                    dep_branchatms = puntos_atencion.atm + puntos_atencion.agencia
                else:
                    dep_branchatms = [
                        bank_branchatm[bankcode](**jitem) for jitem in jdata
                    ]

                branchatms.extend(dep_branchatms)

            continue

        jdata = jdata_from_jsonfile(filename=filepath)

        if bankcode == "bnb":
            departamentos = [BnbDepartamentoRoot(**jitem) for jitem in jdata]
            file_branchatms = [
                BnbBranchATM.model_validate(branchatm)
                for departamento in departamentos
                for branchatm in departamento.detalles
            ]
        else:
            file_branchatms = [bank_branchatm[bankcode](**jitem) for jitem in jdata]

        branchatms.extend(file_branchatms)

    if len(branchatms) > 0:
        filename = f"assets/{bankcode}/branchatms.csv"
        write_data_to_csvfile(filename=filename, data=branchatms)
