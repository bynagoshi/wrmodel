import pandas as pd

df = pd.read_csv("Data/Raw/Combined/draft_wr_2013_2025.csv")
df2 = pd.read_csv("Data/Processed/receiving_wr_2009_2025_by_playerv2.csv")

df = df.merge(df2, left_on=["collegeAthleteId", "name"], right_on=["playerId", "player"], how="left")
df.to_csv("Data/Processed/combined_wr_2013_2025.csv", index=False)