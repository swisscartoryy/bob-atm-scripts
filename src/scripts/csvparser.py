import os
import csv
import json

from typing import get_args

from src.dtos.bg import GanaBranchATM
from src.dtos.bisa import BisaBranchATM
from src.dtos.bmsc import BmscBranchATM

from src.dtos.baneco import BanecoBranchATM
from src.dtos.bancosol import BancoSolBranchATM

from src.dtos.bnb import BnbBranchATM, BnbDepartamentoRoot
from src.dtos.bancounion import BancoUnionBranchATM, BancoUnionPuntosAtencionRoot

from .const import BankCode, BoliviaDepartment

filenames = [
    "atms.json",
    "branches.json",
    "sol_amigo.json",
    "branchatms.json",
    "sol_amigo_express.json",
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


def jdata_from_jsonfile(filename: str):
    with open(filename, mode="r", encoding="utf-8") as jsonfile:
        jdata = json.load(jsonfile)

    return jdata


def write_data_to_csvfile(filename: str, data: list):
    rows = [item.model_dump() for item in data]
    headers = [key for key in data[0].model_dump().keys()]

    with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

        print(filename, "generated")


def generate_bankcsv(bankcode: BankCode) -> str:
    branchatms: list = []

    for filename in filenames:
        filepath = f"assets/{bankcode}/{filename}"

        if not os.path.exists(filepath):
            for department in get_args(BoliviaDepartment):
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

    filename = f"assets/{bankcode}/branchatms.csv"
    write_data_to_csvfile(filename=filename, data=branchatms)

    return filename
