import pandas as pd

def concat_draft_files():
    df = pd.read_csv(f"Data/Raw/draft_wr_2013.csv")

    for year in range(2014, 2026):
        df2 = pd.read_csv(f"Data/Raw/draft_wr_{year}.csv")
        df = pd.concat([df, df2])

    df.to_csv("Data/Raw/Combined/draft_wr_2013_2025.csv", index=False)

def concat_receiving_files():
    df = pd.read_csv(f"Data/Raw/receiving_wr_2009.csv")
    for year in range(2010, 2025):
        df2 = pd.read_csv(f"Data/Raw/receiving_wr_{year}.csv")
        df = pd.concat([df, df2])
    df.to_csv("Data/Raw/Combined/receiving_wr_2009_2025.csv", index=False)

# concat_draft_files()
concat_receiving_files()