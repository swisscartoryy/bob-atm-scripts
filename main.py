import pandas

from typing import get_args
from src.scripts import BankCode, generate_bankcsv

filename = generate_bankcsv("bisa")
data = pandas.read_csv(filename)
print(data)
# for bankcode in get_args(BankCode):
