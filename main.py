import os
import dotenv
import pandas

from typing import get_args
from sqlmodel import SQLModel, create_engine

from src.scripts import BankCode, generate_df
from src.entities import BankServicePointEntity

dotenv.load_dotenv()

engine = create_engine(echo=True, url=os.getenv("DATABASE_URL", ""))
columns_order = list(BankServicePointEntity.model_fields.keys())[1:]

dfs: list[pandas.DataFrame] = []
for bankcode in get_args(BankCode):
    df = generate_df(bankcode).reindex(columns=columns_order)
    dfs.append(df.reset_index(drop=True))
    print(df)

SQLModel.metadata.create_all(engine)
df = pandas.concat(dfs, ignore_index=True)

df.to_csv("assets/branchatms.csv", index=False)
df.to_sql(
    con=engine,
    method="multi",
    chunksize=1000,
    index_label="id",
    if_exists="replace",
    name="bank_service_point",
)
