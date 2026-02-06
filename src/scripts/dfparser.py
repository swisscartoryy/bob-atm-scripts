import pandas

from .csvparser import generate_bankcsv
from .const import BankCode, bank_columns


def generate_df(bankcode: BankCode) -> pandas.DataFrame:
    filename = generate_bankcsv(bankcode)

    df = pandas.read_csv(filename).rename(columns=bank_columns[bankcode])
    df["bankcode"] = str(bankcode).upper()

    if bankcode == "bnb" or bankcode == "bancounion":
        df["name"] = df["description"]
        df["description"] = None

    if bankcode == "bancosol":
        typecol = df["type"].str.replace("_", " ").map(str.title)
        df["type"] = typecol + " " + df["name"]

    return df
