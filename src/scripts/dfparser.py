import pandas

from .csvparser import generate_bankcsv
from .const import BankCode, bank_columns


def generate_df(bankcode: BankCode) -> pandas.DataFrame:
    filename = generate_bankcsv(bankcode)

    df = pandas.read_csv(filename).rename(columns=bank_columns[bankcode])
    df["bankcode"] = bankcode.upper()

    if bankcode == "bnb" or bankcode == "bancounion":
        df["name"] = df["description"]
        df["description"] = None
    elif bankcode == "bisa":
        cond = df["type"].str.startswith("AGENCIA_")
        df.loc[cond, "subtype"] = df["type"]
        df.loc[cond, "type"] = "AGENCIA"
    elif bankcode == "bmsc":
        df["subtype"] = df["type"]
        df["type"] = df["subtype"].str.extract(r"^(AGENCIA|ATM)")
    elif bankcode == "bancosol":
        typecol = df["type"].str.replace("_", " ").map(str.title)
        df["name"] = typecol + " " + df["name"]

    return df
