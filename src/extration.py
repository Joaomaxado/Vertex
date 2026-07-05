import pandas as pd

def extration(file):
    df = pd.read_excel(file)
    return df