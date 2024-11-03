import polars as pl

df = pl.read_csv("./data/generations.csv")
print(df.head())
