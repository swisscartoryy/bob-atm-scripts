import pandas

from typing import get_args
from src.scripts import BankCode, generate_bankcsv

filename = generate_bankcsv("bnb")
data = pandas.read_csv(filename)
print(data.head(20))
# for bankcode in get_args(BankCode):
