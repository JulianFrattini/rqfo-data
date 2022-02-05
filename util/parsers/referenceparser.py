import os
import pandas as pd

def read_records():
    references = pd.read_csv('references/record.csv', sep=',')
    return references