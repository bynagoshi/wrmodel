import pandas as pd

df = pd.read_csv("NFL Data/players_ids.csv")
df = df[df["cfbd_id"].notna()]

df.to_csv("NFL Data/wr_ids.csv", index=False)