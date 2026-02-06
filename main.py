import pandas

from typing import get_args
from src.scripts import BankCode, generate_bankcsv

columns_order = [
    "id",
    "bankcode",
    "type",
    "subtype",
    "name",
    "description",
    "city",
    "address",
    "department",
    "latitude",
    "longitude",
    "phonenumber",
    "opening_hours",
    "additional_info",
]

bank_columns: dict[BankCode, dict[str, str]] = {
    "bg": {
        "tipo": "type",
        "nombre": "name",
        "subtipo": "subtype",
        "latitud": "latitude",
        "direccion": "address",
        "longitud": "longitude",
        "telefono": "phonenumber",
        "descripcion": "description",
    },
    "bnb": {
        "tipo": "type",
        "subtipo": "subtype",
        "latitud": "latitude",
        "direccion": "address",
        "longitud": "longitude",
        "telefonos": "phonenumber",
        "horarios": "opening_hours",
        "descripcion": "description",
        "departamento": "department",
    },
    "bisa": {
        "notes": "additional_info",
        "telephone": "phonenumber",
        "working_hours": "opening_hours",
    },
    "bmsc": {
        "tipo": "type",
        "nombre": "name",
        "ciudad": "city",
        "latitud": "latitude",
        "direccion": "address",
        "longitud": "longitude",
        "telefono": "phonenumber",
        "departamento": "department",
        "horario_atencioncms": "opening_hours",
        "servicios_ofertados": "additional_info",
    },
    "baneco": {
        "tipo": "type",
        "nombre": "name",
        "latitud": "latitude",
        "direccion": "address",
        "longitud": "longitude",
        "telefonos": "phonenumber",
        "horarios": "opening_hours",
        "departamento": "department",
    },
    "bancosol": {
        "phone": "phonenumber",
        "working_hours": "opening_hours",
    },
    "bancounion": {
        "tipo": "type",
        "subtipo": "subtype",
        "latitud": "latitude",
        "longitud": "longitude",
        "direccion": "address",
        "telefono": "phonenumber",
        "descripcion": "description",
        "horario_atencion": "opening_hours",
    },
}

dfs: list[pandas.DataFrame] = []
for bankcode in get_args(BankCode):
    filename = generate_bankcsv(bankcode)

    df = pandas.read_csv(filename).rename(columns=bank_columns[bankcode])
    df["bankcode"] = str(bankcode).upper()

    if bankcode == "bnb" or bankcode == "bancounion":
        df["name"] = df["description"]
        df["description"] = None

    if bankcode == "bancosol":
        typecol = df["type"].str.replace("_", " ").map(str.title)
        df["name"] = typecol + " " + df["name"]

    df = df.reindex(columns=columns_order)
    dfs.append(df.reset_index(drop=True))

    print(df)


pandas.concat(dfs, ignore_index=True).to_csv("assets/branchatms.csv", index=False)
